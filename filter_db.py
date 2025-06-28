from openfilter.filter_runtime.filter import Filter, FilterConfig, Frame
import logging
import cv2
import numpy as np
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def connect_db():
    """Create database connection"""
    load_dotenv()
    try:
        return psycopg2.connect(
            user=os.getenv("user", "postgres"),
            password=os.getenv("password", ""),
            host=os.getenv("host", "localhost"),
            port=os.getenv("port", "5432"),
            dbname=os.getenv("dbname", "postgres")
        )
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


class DBFilterConfig(FilterConfig):
    debug: bool = False

class DBFilter(Filter):
    @classmethod
    def normalize_config(self, config: DBFilterConfig):
        config = DBFilterConfig(super().normalize_config(config))
        return config

    def setup(self, config: DBFilterConfig):
        self.last_person_count = 0
        self.connection = connect_db()
        logger.info(f"DBFilter setup with config: {config}")
    
    def log_change(self, current, previous):
        """Log person count changes to database"""
        if not self.connection or current == previous:
            return
        
        try:
            change_type = "increase" if current > previous else "decrease"
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO openfilter_example (current_count, notes) VALUES (%s, %s)",
                (current, f"Person count {change_type}d from {previous} to {current}")
            )
            self.connection.commit()
            cursor.close()
            logger.info(f"Logged person count {change_type}: {previous} -> {current}")
        except Exception as e:
            logger.error(f"Database logging failed: {e}")
            self.connection = connect_db()  

    def process(self, frames: dict[str, Frame]):
        frame = frames.get('main')
        image = frame.rw_rgb.image
        objects = frame.data['objects']

        # Count objects (filter persons by confidence > 0.7)
        class_counts = {}
        for obj in objects:
            if obj['class'] == 'person' and obj['confidence'] <= 0.7:
                continue
            class_counts[obj['class']] = class_counts.get(obj['class'], 0) + 1
        
        # Log person count changes
        current_person_count = class_counts.get('person', 0)
        if current_person_count != self.last_person_count:
            self.log_change(current_person_count, self.last_person_count)
            self.last_person_count = current_person_count
        
        # Create text overlay
        text = f"Objects: {len(objects)}"
        for class_name, count in class_counts.items():
            text += f" | {class_name}: {count}"
        
        cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        frames['main'] = Frame(image, {**frame.data}, format='RGB')
      
        return frames

if __name__ == "__main__":
    DBFilter.run()
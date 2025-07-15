"""
Business Doctor Data Pipeline
Handles data flow, processing, and transformation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import sqlite3
from datetime import datetime
import hashlib
import os

@dataclass
class DataRecord:
    """Base data record for pipeline processing"""
    id: str
    timestamp: datetime
    record_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "record_type": self.record_type,
            "data": self.data,
            "metadata": self.metadata
        }

class DataPipeline:
    """Main data pipeline for Business Doctor system"""
    
    def __init__(self, db_path: str = "business_doctor.db"):
        """Initialize pipeline with database"""
        self.db_path = db_path
        self._init_database()
        self.processors = {}
        self.validators = {}
        
    def _init_database(self):
        """Initialize SQLite database for data persistence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Consultations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                company_name TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT,
                conversation_data TEXT,
                metrics_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Bottlenecks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bottlenecks (
                id TEXT PRIMARY KEY,
                consultation_id TEXT,
                name TEXT,
                description TEXT,
                department TEXT,
                frequency TEXT,
                time_impact_hours REAL,
                cost_impact REAL,
                automation_potential REAL,
                priority TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id)
            )
        """)
        
        # Insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                id TEXT PRIMARY KEY,
                consultation_id TEXT,
                category TEXT,
                insight TEXT,
                confidence REAL,
                potential_value REAL,
                implementation_effort TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id)
            )
        """)
        
        # Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                consultation_id TEXT,
                report_type TEXT,
                report_data TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_processor(self, record_type: str, processor_func):
        """Register a data processor for specific record type"""
        self.processors[record_type] = processor_func
    
    def register_validator(self, record_type: str, validator_func):
        """Register a data validator for specific record type"""
        self.validators[record_type] = validator_func
    
    def process(self, record: DataRecord) -> Optional[DataRecord]:
        """Process a data record through the pipeline"""
        # Validate
        if validator := self.validators.get(record.record_type):
            if not validator(record):
                raise ValueError(f"Validation failed for record type: {record.record_type}")
        
        # Process
        if processor := self.processors.get(record.record_type):
            record = processor(record)
        
        # Store
        self._store_record(record)
        
        return record
    
    def _store_record(self, record: DataRecord):
        """Store record in appropriate table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if record.record_type == "consultation":
                self._store_consultation(cursor, record)
            elif record.record_type == "bottleneck":
                self._store_bottleneck(cursor, record)
            elif record.record_type == "insight":
                self._store_insight(cursor, record)
            elif record.record_type == "report":
                self._store_report(cursor, record)
            
            conn.commit()
        finally:
            conn.close()
    
    def _store_consultation(self, cursor, record: DataRecord):
        """Store consultation record"""
        data = record.data
        cursor.execute("""
            INSERT OR REPLACE INTO consultations 
            (id, client_id, company_name, start_time, end_time, status, 
             conversation_data, metrics_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.id,
            data.get("client_id"),
            data.get("company_name"),
            data.get("start_time"),
            data.get("end_time"),
            data.get("status", "in_progress"),
            json.dumps(data.get("conversation", [])),
            json.dumps(data.get("metrics", {}))
        ))
    
    def _store_bottleneck(self, cursor, record: DataRecord):
        """Store bottleneck record"""
        data = record.data
        cursor.execute("""
            INSERT INTO bottlenecks 
            (id, consultation_id, name, description, department, frequency,
             time_impact_hours, cost_impact, automation_potential, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.id,
            data.get("consultation_id"),
            data.get("name"),
            data.get("description"),
            data.get("department"),
            data.get("frequency"),
            data.get("time_impact_hours"),
            data.get("cost_impact"),
            data.get("automation_potential"),
            data.get("priority")
        ))
    
    def _store_insight(self, cursor, record: DataRecord):
        """Store insight record"""
        data = record.data
        cursor.execute("""
            INSERT INTO insights 
            (id, consultation_id, category, insight, confidence,
             potential_value, implementation_effort)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            record.id,
            data.get("consultation_id"),
            data.get("category"),
            data.get("insight"),
            data.get("confidence"),
            data.get("potential_value"),
            data.get("implementation_effort")
        ))
    
    def _store_report(self, cursor, record: DataRecord):
        """Store report record"""
        data = record.data
        cursor.execute("""
            INSERT INTO reports 
            (id, consultation_id, report_type, report_data)
            VALUES (?, ?, ?, ?)
        """, (
            record.id,
            data.get("consultation_id"),
            data.get("report_type"),
            json.dumps(data.get("report_data", {}))
        ))
    
    def get_consultation(self, consultation_id: str) -> Optional[Dict]:
        """Retrieve consultation by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM consultations WHERE id = ?
        """, (consultation_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            consultation = dict(zip(columns, row))
            consultation['conversation_data'] = json.loads(consultation['conversation_data'])
            consultation['metrics_data'] = json.loads(consultation['metrics_data'])
            return consultation
        return None
    
    def get_bottlenecks(self, consultation_id: str) -> List[Dict]:
        """Get all bottlenecks for a consultation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM bottlenecks WHERE consultation_id = ?
            ORDER BY cost_impact DESC
        """, (consultation_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_insights(self, consultation_id: str) -> List[Dict]:
        """Get all insights for a consultation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM insights WHERE consultation_id = ?
            ORDER BY potential_value DESC
        """, (consultation_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_report(self, consultation_id: str, report_type: str = "diagnostic") -> Optional[Dict]:
        """Get report for consultation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM reports 
            WHERE consultation_id = ? AND report_type = ?
            ORDER BY generated_at DESC
            LIMIT 1
        """, (consultation_id, report_type))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            report = dict(zip(columns, row))
            report['report_data'] = json.loads(report['report_data'])
            return report
        return None

class DataProcessors:
    """Collection of data processing functions"""
    
    @staticmethod
    def process_consultation(record: DataRecord) -> DataRecord:
        """Process consultation data"""
        # Add consultation ID if not present
        if not record.id:
            record.id = DataProcessors.generate_id("consultation", record.data)
        
        # Add timestamps
        if "start_time" not in record.data:
            record.data["start_time"] = datetime.now().isoformat()
        
        # Initialize empty arrays if needed
        if "conversation" not in record.data:
            record.data["conversation"] = []
        if "metrics" not in record.data:
            record.data["metrics"] = {}
        
        return record
    
    @staticmethod
    def process_bottleneck(record: DataRecord) -> DataRecord:
        """Process bottleneck data"""
        # Generate ID
        if not record.id:
            record.id = DataProcessors.generate_id("bottleneck", record.data)
        
        # Calculate annual impact
        data = record.data
        frequency_multiplier = {
            "daily": 250,
            "weekly": 52,
            "monthly": 12,
            "quarterly": 4
        }
        
        multiplier = frequency_multiplier.get(data.get("frequency", "weekly"), 52)
        data["annual_hours_impact"] = data.get("time_impact_hours", 0) * multiplier
        data["annual_cost_impact"] = data.get("cost_impact", 0) * multiplier
        
        # Set default priority based on impact
        if "priority" not in data:
            if data["annual_cost_impact"] > 100000:
                data["priority"] = "critical"
            elif data["annual_cost_impact"] > 50000:
                data["priority"] = "high"
            elif data["annual_cost_impact"] > 10000:
                data["priority"] = "medium"
            else:
                data["priority"] = "low"
        
        return record
    
    @staticmethod
    def process_insight(record: DataRecord) -> DataRecord:
        """Process insight data"""
        # Generate ID
        if not record.id:
            record.id = DataProcessors.generate_id("insight", record.data)
        
        # Calculate priority score
        data = record.data
        effort_multiplier = {"low": 1.5, "medium": 1.0, "high": 0.5}
        
        confidence = data.get("confidence", 0.5)
        value = data.get("potential_value", 0)
        effort = data.get("implementation_effort", "medium")
        
        data["priority_score"] = value * confidence * effort_multiplier.get(effort, 1.0)
        
        return record
    
    @staticmethod
    def generate_id(prefix: str, data: Dict) -> str:
        """Generate unique ID for record"""
        # Create hash from data
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}_{hash_obj.hexdigest()[:8]}_{int(datetime.now().timestamp())}"

class DataValidators:
    """Collection of data validation functions"""
    
    @staticmethod
    def validate_consultation(record: DataRecord) -> bool:
        """Validate consultation record"""
        required_fields = ["client_id"]
        data = record.data
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        return True
    
    @staticmethod
    def validate_bottleneck(record: DataRecord) -> bool:
        """Validate bottleneck record"""
        required_fields = ["consultation_id", "name", "time_impact_hours", "cost_impact"]
        data = record.data
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate numeric fields
        try:
            float(data["time_impact_hours"])
            float(data["cost_impact"])
        except (ValueError, TypeError):
            return False
        
        return True
    
    @staticmethod
    def validate_insight(record: DataRecord) -> bool:
        """Validate insight record"""
        required_fields = ["consultation_id", "insight", "confidence"]
        data = record.data
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate confidence is between 0 and 1
        confidence = data.get("confidence", 0)
        if not 0 <= confidence <= 1:
            return False
        
        return True

# Pipeline factory function
def create_pipeline(db_path: str = "business_doctor.db") -> DataPipeline:
    """Create and configure data pipeline"""
    pipeline = DataPipeline(db_path)
    
    # Register processors
    pipeline.register_processor("consultation", DataProcessors.process_consultation)
    pipeline.register_processor("bottleneck", DataProcessors.process_bottleneck)
    pipeline.register_processor("insight", DataProcessors.process_insight)
    
    # Register validators
    pipeline.register_validator("consultation", DataValidators.validate_consultation)
    pipeline.register_validator("bottleneck", DataValidators.validate_bottleneck)
    pipeline.register_validator("insight", DataValidators.validate_insight)
    
    return pipeline

# Example usage
if __name__ == "__main__":
    # Create pipeline
    pipeline = create_pipeline()
    
    # Create sample consultation
    consultation = DataRecord(
        id="",
        timestamp=datetime.now(),
        record_type="consultation",
        data={
            "client_id": "client_123",
            "company_name": "Test Company LLC",
            "conversation": [],
            "metrics": {"employees": 50}
        }
    )
    
    # Process consultation
    processed = pipeline.process(consultation)
    print(f"Consultation ID: {processed.id}")
    
    # Add bottleneck
    bottleneck = DataRecord(
        id="",
        timestamp=datetime.now(),
        record_type="bottleneck",
        data={
            "consultation_id": processed.id,
            "name": "Manual invoice processing",
            "description": "Invoices processed manually in Excel",
            "department": "Finance",
            "frequency": "daily",
            "time_impact_hours": 3,
            "cost_impact": 225,
            "automation_potential": 0.9
        }
    )
    
    pipeline.process(bottleneck)
    
    # Retrieve data
    saved_consultation = pipeline.get_consultation(processed.id)
    bottlenecks = pipeline.get_bottlenecks(processed.id)
    
    print(f"Retrieved consultation: {saved_consultation['company_name']}")
    print(f"Bottlenecks found: {len(bottlenecks)}")
    for b in bottlenecks:
        print(f"  - {b['name']}: ${b['annual_cost_impact']:,.0f}/year")
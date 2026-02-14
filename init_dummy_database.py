"""
Comprehensive Database Initialization
Creates a realistic test database with industries, companies, persons, and use cases.
"""

import os
from models.base import Base, engine, SessionLocal
from models import Industry, Company, Person, UseCase

def delete_existing_db():
    """Delete the existing database file if it exists."""
    db_file = 'use_cases.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✓ Deleted existing database: {db_file}")

def create_comprehensive_data():
    """Create a comprehensive test database."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Created database tables")
    
    db = SessionLocal()
    
    try:
        # ===== INDUSTRIES =====
        print("\n1. Creating industries...")
        energy = Industry(name="Energy")
        manufacturing = Industry(name="Manufacturing")
        healthcare = Industry(name="Healthcare")
        
        db.add_all([energy, manufacturing, healthcare])
        db.commit()
        print(f"   ✓ Created {3} industries")
        
        # ===== COMPANIES =====
        print("\n2. Creating companies...")
        companies_data = [
            # Energy
            ("Siemens Energy", energy.id),
            ("E.ON", energy.id),
            ("RWE", energy.id),
            # Manufacturing
            ("Bosch", manufacturing.id),
            ("Schaeffler", manufacturing.id),
            ("Trumpf", manufacturing.id),
            # Healthcare
            ("Charité Berlin", healthcare.id),
            ("Helios Kliniken", healthcare.id),
            ("Universitätsklinikum Freiburg", healthcare.id),
        ]
        
        companies = []
        for name, industry_id in companies_data:
            comp = Company(name=name, industry_id=industry_id)
            companies.append(comp)
        
        db.add_all(companies)
        db.commit()
        print(f"   ✓ Created {len(companies)} companies")
        
        # ===== PERSONS =====
        print("\n3. Creating persons...")
        persons_data = [
            # Siemens Energy
            ("Anna Schmidt", "CTO", companies[0].id),
            ("Michael Weber", "Head of AI", companies[0].id),
            # E.ON
            ("Lisa Müller", "Innovation Manager", companies[1].id),
            ("Thomas Klein", "Data Science Lead", companies[1].id),
            # RWE
            ("Sarah Fischer", "Digital Transformation Officer", companies[2].id),
            # Bosch
            ("Martin Becker", "VP Engineering", companies[3].id),
            ("Julia Schneider", "IoT Architect", companies[3].id),
            # Schaeffler
            ("David Koch", "Head of Innovation", companies[4].id),
            # Trumpf
            ("Laura Meyer", "AI Research Lead", companies[5].id),
            # Charité
            ("Dr. Frank Wagner", "Chief Medical Officer", companies[6].id),
            ("Nina Hoffmann", "IT Director", companies[6].id),
            # Helios
            ("Dr. Stefan Richter", "Head of Digitalization", companies[7].id),
            # Uni Freiburg
            ("Prof. Maria Zimmermann", "Director of Medical IT", companies[8].id),
        ]
        
        persons = []
        for name, role, company_id in persons_data:
            person = Person(name=name, role=role, company_id=company_id)
            persons.append(person)
        
        db.add_all(persons)
        db.commit()
        print(f"   ✓ Created {len(persons)} persons")
        
        # ===== USE CASES =====
        print("\n4. Creating use cases...")
        use_cases_data = [
            # Energy sector
            {
                "title": "Smart Grid Optimization with AI",
                "description": "Machine learning algorithms to optimize energy distribution in real-time based on consumption patterns and renewable energy availability.",
                "expected_benefit": "Reduce energy waste by 15-20%, improve grid stability, better integration of renewable sources",
                "status": "in_progress",
                "company_id": companies[0].id,  # Siemens Energy
                "industry_id": energy.id,
                "person_ids": [0, 1]  # Anna, Michael
            },
            {
                "title": "Predictive Maintenance for Wind Turbines",
                "description": "IoT sensors combined with AI to predict maintenance needs before failures occur, reducing downtime.",
                "expected_benefit": "Reduce downtime by 30%, extend equipment lifetime by 20%, lower maintenance costs",
                "status": "approved",
                "company_id": companies[0].id,  # Siemens Energy
                "industry_id": energy.id,
                "person_ids": [0]  # Anna
            },
            {
                "title": "Energy Consumption Forecasting",
                "description": "AI-powered forecasting of energy consumption patterns for better capacity planning and pricing strategies.",
                "expected_benefit": "Improve demand prediction accuracy by 25%, optimize pricing, reduce peak load issues",
                "status": "new",
                "company_id": companies[1].id,  # E.ON
                "industry_id": energy.id,
                "person_ids": [2, 3]  # Lisa, Thomas
            },
            {
                "title": "Carbon Emissions Tracking Platform",
                "description": "Real-time tracking and reporting of carbon emissions across all generation facilities with AI-powered optimization suggestions.",
                "expected_benefit": "Meet regulatory requirements, reduce carbon footprint by 10%, improve ESG ratings",
                "status": "in_review",
                "company_id": companies[2].id,  # RWE
                "industry_id": energy.id,
                "person_ids": [4]  # Sarah
            },
            
            # Manufacturing sector
            {
                "title": "Computer Vision Quality Control",
                "description": "Automated defect detection on production lines using computer vision and deep learning.",
                "expected_benefit": "99.5% defect detection rate, reduce manual inspection time by 80%, improve product quality",
                "status": "in_progress",
                "company_id": companies[3].id,  # Bosch
                "industry_id": manufacturing.id,
                "person_ids": [5, 6]  # Martin, Julia
            },
            {
                "title": "Predictive Equipment Failure Detection",
                "description": "Machine learning models analyzing sensor data to predict equipment failures before they occur.",
                "expected_benefit": "Reduce unplanned downtime by 40%, lower maintenance costs by 25%",
                "status": "approved",
                "company_id": companies[3].id,  # Bosch
                "industry_id": manufacturing.id,
                "person_ids": [6]  # Julia
            },
            {
                "title": "Supply Chain Optimization AI",
                "description": "AI system optimizing supply chain logistics, inventory levels, and supplier selection.",
                "expected_benefit": "Reduce inventory costs by 20%, improve delivery times by 15%, minimize stockouts",
                "status": "new",
                "company_id": companies[4].id,  # Schaeffler
                "industry_id": manufacturing.id,
                "person_ids": [7]  # David
            },
            {
                "title": "Laser Cutting Parameter Optimization",
                "description": "AI-powered optimization of laser cutting parameters for different materials and thicknesses.",
                "expected_benefit": "Improve cutting quality, reduce material waste by 12%, increase throughput by 18%",
                "status": "in_progress",
                "company_id": companies[5].id,  # Trumpf
                "industry_id": manufacturing.id,
                "person_ids": [8]  # Laura
            },
            
            # Healthcare sector
            {
                "title": "AI-Assisted Radiology Diagnosis",
                "description": "Deep learning models to assist radiologists in detecting anomalies in X-rays, CT scans, and MRIs.",
                "expected_benefit": "Improve diagnostic accuracy by 15%, reduce radiologist workload, faster turnaround times",
                "status": "in_review",
                "company_id": companies[6].id,  # Charité
                "industry_id": healthcare.id,
                "person_ids": [9, 10]  # Dr. Wagner, Nina
            },
            {
                "title": "Patient Flow Optimization",
                "description": "AI system to optimize patient scheduling, bed allocation, and resource distribution across departments.",
                "expected_benefit": "Reduce patient wait times by 25%, improve bed utilization by 20%, better resource allocation",
                "status": "approved",
                "company_id": companies[7].id,  # Helios
                "industry_id": healthcare.id,
                "person_ids": [11]  # Dr. Richter
            },
            {
                "title": "Clinical Decision Support System",
                "description": "AI-powered system providing evidence-based treatment recommendations based on patient data and latest research.",
                "expected_benefit": "Improve treatment outcomes, reduce medical errors, support junior doctors",
                "status": "new",
                "company_id": companies[8].id,  # Uni Freiburg
                "industry_id": healthcare.id,
                "person_ids": [12]  # Prof. Zimmermann
            },
        ]
        
        use_cases = []
        for uc_data in use_cases_data:
            person_ids = uc_data.pop("person_ids")
            
            uc = UseCase(**uc_data)
            db.add(uc)  # ← Add to session FIRST
            
            # Now add contributing persons (SQLAlchemy tracks this)
            for person_idx in person_ids:
                uc.persons.append(persons[person_idx])
            
            use_cases.append(uc)

        db.commit()  # Commit once at the end
        print(f"   ✓ Created {len(use_cases)} use cases with person assignments")
        
        # ===== SUMMARY =====
        print("\n" + "="*60)
        print("DATABASE CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"Industries:  {len([energy, manufacturing, healthcare])}")
        print(f"Companies:   {len(companies)}")
        print(f"Persons:     {len(persons)}")
        print(f"Use Cases:   {len(use_cases)}")
        print("="*60)
        
        # Show sample data
        print("\nSample Data:")
        print(f"\nEnergy Industry Companies:")
        for comp in companies[:3]:
            print(f"  - {comp.name}")
        
        print(f"\nManufacturing Industry Companies:")
        for comp in companies[3:6]:
            print(f"  - {comp.name}")
        
        print(f"\nHealthcare Industry Companies:")
        for comp in companies[6:9]:
            print(f"  - {comp.name}")
        
        print(f"\nSample Use Cases:")
        for uc in use_cases[:3]:
            contributors = ", ".join([p.name for p in uc.persons])
            print(f"  - {uc.title} ({uc.company.name})")
            print(f"    Contributors: {contributors}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("="*60)
    print("COMPREHENSIVE DATABASE INITIALIZATION")
    print("="*60)
    print("\nThis will DELETE the existing database and create a new one.")
    
    confirm = input("\nContinue? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        delete_existing_db()
        create_comprehensive_data()
        print("\n✓ Done! You can now use the database for testing.")
    else:
        print("\nCancelled.")
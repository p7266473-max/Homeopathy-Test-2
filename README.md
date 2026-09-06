# Homeopathy-Test-2: Clinical Intake & Consultation System

A comprehensive Streamlit web application designed for classical homeopathic case-taking, symptom modality evaluation, and prescription management.

## Features
- **Patient Intake Questionnaire:** Detailed multi-section form covering demographics, chief complaints, sensations, onset triggers, physical generals (thermals, thirst, cravings), mind & temperament, and modalities (worse/better by).
- **Data Persistence:** Consultation records are saved locally as structured JSON files (`consultations/`) and indexed in an SQLite database (`homeopathy.db`).
- **Doctor Review & Remedy Prescriber:** Review complete constitutional case files and leverage an integrated Materia Medica remedy intelligence engine (matching remedies like *Arsenicum Album*, *Pulsatilla*, *Bryonia*, *Nux Vomica*, *Rhus Tox*, *Belladonna*).
- **Records Directory & Analytics:** Searchable table of past patient records with CSV export capabilities.

## Launch Instructions
```bash
streamlit run app.py
```

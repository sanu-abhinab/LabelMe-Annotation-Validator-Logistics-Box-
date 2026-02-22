# LabelMe-Annotation-Validator-Logistics-Box-
Perfect 👌 Below is a **clean, professional README.md** ready to paste into GitHub.

It is:

* Clear
* Internship-ready
* Industry-style
* Not overly long
* Properly structured

---

# 📦 LabelMe Annotation Validator

## 📌 Overview

**LabelMe Annotation Validator** is a rule-based quality control tool designed to validate rectangle annotations for logistics conveyor belt box datasets.

The tool automatically detects:

* Structural JSON errors
* Overlapping labels
* Unrealistic bounding boxes
* Missing annotation files
* Empty annotation files
* Unannotated images

It separates invalid samples into dedicated folders for efficient dataset cleaning.

This tool is intended for **annotation quality assurance (QA)** before training computer vision models.

---

## 🚀 Features

✔ Structural validation of LabelMe JSON files
✔ Bounding box geometry sanity checks
✔ Overlap detection (strict intersection-based logic)
✔ Detection of unrealistic bounding boxes
✔ Detection of missing JSON files
✔ Automatic separation of invalid samples
✔ Can be converted into standalone `.exe`

---

## 📂 Folder Behavior

When executed inside a folder containing images and JSON files, the program automatically creates:

```
defects/
manual_verification/
no_json/
```

### File Routing Logic

| Scenario                     | Action                     |
| ---------------------------- | -------------------------- |
| Overlapping labels           | → `defects/`               |
| Unrealistic or invalid boxes | → `defects/`               |
| Structural JSON error        | → `defects/`               |
| Empty JSON (no boxes)        | → `manual_verification/`   |
| Image without JSON           | → `no_json/`               |
| Valid annotation             | Remains in original folder |

---

## 🛠 Requirements

* Python 3.x
* OpenCV

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶ How to Use (Python Version)

1. Place `validator.py` inside a folder containing images and JSON files.
2. Double-click the script or run:

```bash
python validator.py
```

3. The program will automatically process files and separate invalid samples.

---

## 🖥 How to Use (.exe Version)

1. Place `validator.exe` inside the dataset folder.
2. Double-click it.
3. The program runs automatically and creates output folders.

No Python installation is required for the `.exe` version.

---

## ⚙ Validation Logic Summary

The validator follows a multi-layered approach:

1. Structural validation of JSON format
2. Bounding box extraction
3. Geometry validation:

   * Minimum area threshold
   * Maximum area threshold
   * Aspect ratio sanity
   * Location constraint (conveyor zone check)
4. Strict overlap detection (no intersection allowed)
5. Folder-based routing for dataset cleaning

---

## 🎯 Use Case

This tool is useful for:

* Logistics conveyor belt datasets
* Pre-training dataset validation
* Annotation QA pipelines
* Internship / academic computer vision projects

---

## 📎 Project Status

✔ Rule-based implementation
✔ Fully automated separation logic
✔ Deployment-ready as executable

---

## 📜 License

This project is for educational and research purposes.



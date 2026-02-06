"""Association Types - Unidirectional and Bidirectional relationships."""


# === UNIDIRECTIONAL ASSOCIATION ===
# Student knows about Course, but Course doesn't know about Student

class Course:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"{self.code}: {self.name}"


class Student:
    """Student knows its enrolled courses (unidirectional)."""

    def __init__(self, name: str):
        self.name = name
        self.courses: list[Course] = []

    def enroll(self, course: Course) -> None:
        self.courses.append(course)

    def show_courses(self) -> None:
        names = [c.code for c in self.courses]
        print(f"  {self.name} enrolled in: {names}")


# === BIDIRECTIONAL ASSOCIATION ===
# Doctor and Patient each know about the other

class Patient:
    def __init__(self, name: str):
        self.name = name
        self.doctors: list["Doctor"] = []

    def show_doctors(self) -> None:
        names = [d.name for d in self.doctors]
        print(f"  Patient {self.name}'s doctors: {names}")


class Doctor:
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.patients: list[Patient] = []

    def add_patient(self, patient: Patient) -> None:
        """Maintains both sides of the relationship."""
        if patient not in self.patients:
            self.patients.append(patient)
            patient.doctors.append(self)

    def show_patients(self) -> None:
        names = [p.name for p in self.patients]
        print(f"  Dr. {self.name} ({self.specialty}): {names}")


if __name__ == "__main__":
    print("=== Association Types ===\n")

    # Unidirectional: Student -> Course
    print("--- Unidirectional (Student -> Course) ---")
    math = Course("Mathematics", "MATH101")
    physics = Course("Physics", "PHY101")

    alice = Student("Alice")
    alice.enroll(math)
    alice.enroll(physics)
    alice.show_courses()
    print(f"  Course knows students? No. Course has no student list.\n")

    # Bidirectional: Doctor <-> Patient
    print("--- Bidirectional (Doctor <-> Patient) ---")
    dr_smith = Doctor("Smith", "Cardiology")
    dr_jones = Doctor("Jones", "Neurology")

    pat_bob = Patient("Bob")
    pat_carol = Patient("Carol")

    dr_smith.add_patient(pat_bob)
    dr_smith.add_patient(pat_carol)
    dr_jones.add_patient(pat_bob)  # Bob sees two doctors

    dr_smith.show_patients()
    dr_jones.show_patients()
    pat_bob.show_doctors()
    pat_carol.show_doctors()

    print("\n--- Summary ---")
    print("  Unidirectional: A -> B (A knows B, B doesn't know A)")
    print("  Bidirectional:  A <-> B (both know each other)")

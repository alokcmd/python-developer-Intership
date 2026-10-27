
import unittest


def calculate_grade(marks):
    if not 0 <= marks <= 100:
        raise ValueError("Marks must be between 0 and 100")

    if marks >= 80:
        return "A"
    elif marks >= 60:
        return "B"
    else:
        return "C"


class TestCalculateGrade(unittest.TestCase):

    def test_grade_a(self):
        self.assertEqual(calculate_grade(85), "A")

    def test_grade_b(self):
        self.assertEqual(calculate_grade(65), "B")

    def test_grade_c(self):
        self.assertEqual(calculate_grade(40), "C")

    def test_boundary_marks(self):
        self.assertEqual(calculate_grade(80), "A")
        self.assertEqual(calculate_grade(60), "B")
        self.assertEqual(calculate_grade(0), "C")
        self.assertEqual(calculate_grade(100), "A")

    def test_invalid_marks(self):
        with self.assertRaises(ValueError):
            calculate_grade(-1)

        with self.assertRaises(ValueError):
            calculate_grade(101)


if __name__ == "__main__":
    unittest.main()

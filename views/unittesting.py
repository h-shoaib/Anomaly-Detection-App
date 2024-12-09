import unittest
import streamlit
from analysis import extract_features, calculate_similarity, compare_with_existing_pdfs
from file_upload import process_document, analyze_pdf_handwriting

class TestFile1(unittest.TestCase):
    def setUp(self):
        # Set up test data for feature extraction and comparison
        self.sample_text = "This is a test document. It contains sentences with various words for analysis."
        self.pdf_features = {
            'pdf1': {
                'readability_score': 14.8,
                'lexical_diversity': 0.72,
                'sentence_count': 32,
                'avg_sentence_length': 18.4,
                'noun_percentage': 0.40,
                'verb_percentage': 0.22,
                'adj_percentage': 0.16,
                'other_percentage': 0.22
            }
        }
   
    def test_extract_features(self):
        # Test extract_features with real text input
        features = extract_features(self.sample_text)
        self.assertIn('readability_score', features)
        self.assertIn('lexical_diversity', features)
        self.assertGreater(features['readability_score'], 0)

    def test_calculate_similarity(self):
        # Test calculate_similarity with real feature data
        pdf1_features = self.pdf_features['pdf1']
        pdf2_features = self.pdf_features['pdf1']  # Using identical data for simplicity
        similarity = calculate_similarity(pdf1_features, pdf2_features)
        self.assertAlmostEqual(similarity, 1.0, places=2)  # Identical inputs should give similarity = 1.0

    def test_compare_with_existing_pdfs(self):
        # Test compare_with_existing_pdfs with realistic inputs
        results = compare_with_existing_pdfs(self.sample_text, self.pdf_features)
        self.assertIn('pdf1', results)
        self.assertGreaterEqual(results['pdf1'], 0)
        self.assertLessEqual(results['pdf1'], 1)


class TestFile2(unittest.TestCase):
    def setUp(self):
        # Set up test data for PDF processing and handwriting analysis
        self.pdf_content = b"%PDF-1.4\n% Test PDF content for analysis.\n..."  # Example PDF content in bytes
   
    def test_process_document(self):
        # Test process_document with real PDF bytes
        extracted_text = process_document(self.pdf_content)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)

    def test_analyze_pdf_handwriting(self):
        # Test analyze_pdf_handwriting with real PDF bytes
        handwriting_analysis = analyze_pdf_handwriting(self.pdf_content)
        self.assertIsInstance(handwriting_analysis, str)
        self.assertIn("Handwriting Anomaly Detected", handwriting_analysis)


if __name__ == '__main__':
    unittest.main()
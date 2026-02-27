import unittest
from fdtdx_studio.ui.attribute_definitions import OBJECT_DEFINITIONS, AttributeDef
# Mocking nicegui and other dependencies would be needed for full AutoConfigPanel testing
# For now, we verify the metadata structure and key definitions.

class TestUIGeneration(unittest.TestCase):
    def test_object_definitions_consistency(self):
        """Verify that all definitions follow the expected structure."""
        for key, defs in OBJECT_DEFINITIONS.items():
            self.assertIsInstance(defs, list, f"Definitions for {key} should be a list")
            for attr in defs:
                self.assertIsInstance(attr, AttributeDef, f"Content of {key} should be AttributeDef")
                self.assertTrue(attr.name, f"Attribute name missing in {key}")
                self.assertTrue(attr.label, f"Attribute label missing in {key} for {attr.name}")
                self.assertTrue(attr.ui_type, f"Attribute ui_type missing in {key} for {attr.name}")
                self.assertIn(attr.ui_type, ['number', 'string', 'boolean', 'select', 'multi_select', 'color', 'nested', 'vector3', 'material_select'], 
                              f"Invalid ui_type {attr.ui_type} in {key}")
    
    def test_gaussian_source_attributes(self):
        """Verify GaussianPlaneSource has expected attributes."""
        defs = {d.name: d for d in OBJECT_DEFINITIONS['GaussianPlaneSource']}
        self.assertIn('direction', defs)
        self.assertIn('fixed_E_polarization_vector', defs)
        self.assertEqual(defs['fixed_E_polarization_vector'].ui_type, 'vector3')
        self.assertIn('radius', defs)

    def test_detectors_have_common_attributes(self):
        """Verify detectors have shared attributes."""
        detectors = ['FieldDetector', 'EnergyDetector', 'PoyntingFluxDetector', 'PhasorDetector', 'ModeOverlapDetector']
        common_attrs = ['dtype', 'exact_interpolation', 'inverse', 'num_video_workers']
        
        for det in detectors:
            defs = {d.name: d for d in OBJECT_DEFINITIONS[det]}
            for attr in common_attrs:
                self.assertIn(attr, defs, f"{det} missing common attribute {attr}")

if __name__ == '__main__':
    unittest.main()

Feature: Model Processing
  As a user of noah123d
  I want to process STL model files
  So that I can build assemblies from 3D models

  Background:
    Given I have sample STL files available

  Scenario: Load a single valid STL model
    Given a valid STL file "cube.stl" exists
    When I process the model file "cube.stl"
    Then the model should be loaded successfully
    And I should see confirmation that the model was loaded
    And the model should be moved to origin

  Scenario: Process multiple models
    Given valid STL files "cube.stl" and "sphere.stl" exist
    When I process multiple model files
    Then both models should be loaded successfully
    And I should see confirmation for each model
    And no duplicate loading should occur

  Scenario: Process models from directory
    Given a directory "test_models" contains STL files
    When I process all models from the directory
    Then all STL files in the directory should be processed
    And I should see a directory search message

  Scenario: Verbose model processing
    Given a valid STL file "cube.stl" exists
    When I process the model with verbose output enabled
    Then I should see detailed mesh information
    And I should see mesh bounds information
    And I should see triangle count information

  @integration
  Scenario: Model transformation validation
    Given a valid STL file positioned away from origin
    When I process the model file
    Then the model should be moved to origin coordinates
    And the bounding box minimum should be at (0,0,0)

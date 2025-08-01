Feature: CLI Basic Operations (pytest-bdd version)
  As a user of noah123d
  I want to interact with the command-line interface
  So that I can process 3D models effectively

  Scenario: Display help information
    When I run noah123d with "--help" option
    Then I should see the help message
    And the help should contain "Noah123d - CLI for building assemblies from STL models"

  Scenario: Display version information
    When I run noah123d with "--version" option
    Then I should see version information displayed
    And the version format should be valid

  Scenario: Run with no arguments shows guidance
    When I run noah123d with no arguments
    Then I should see "No models loaded" message
    And I should see guidance about using "--model" option

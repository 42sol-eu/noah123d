Feature: CLI Basic Functionality
  As a user of noah123d
  I want to interact with the command-line interface
  So that I can process 3D models effectively

  Background:
    Given the noah123d CLI is available

  Scenario: Display help information
    When I run the command with "--help" option
    Then I should see the help text
    And the help text should contain "Noah123d - CLI for building assemblies from STL models"
    And the exit code should be 0

  Scenario: Display version information
    When I run the command with "--version" option
    Then I should see the version information
    And the version should match the expected format
    And the exit code should be 0

  Scenario: Run with no arguments
    When I run the command with no arguments
    Then I should see a message about no models loaded
    And the message should suggest using "--model" option
    And the exit code should be 0

  @slow
  Scenario: Invalid model file
    When I run the command with model "nonexistent.stl"
    Then I should see an error message about file not found
    And the exit code should be 0

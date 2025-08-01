Feature: Error Handling
  As a user of noah123d
  I want the application to handle errors gracefully
  So that I get meaningful feedback when things go wrong

  Scenario Outline: Invalid file handling
    Given an invalid file "<filename>"
    When I try to process the file
    Then I should see an appropriate error message
    And the application should continue running

    Examples:
      | filename        |
      | nonexistent.stl |
      | empty.stl       |
      | corrupt.stl     |

  Scenario: Invalid directory handling
    Given a directory that does not exist
    When I try to process models from the directory
    Then I should see a directory not found error
    And the application should handle it gracefully

  Scenario: Permission denied
    Given a file that cannot be read due to permissions
    When I try to process the file
    Then I should see a permission error message
    And the application should continue

  Scenario: Invalid mesh data
    Given a file with invalid mesh data
    When I try to process the file
    Then I should see a mesh loading error
    And the error should be descriptive

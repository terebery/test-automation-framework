Feature: User
  Scenario: TC_01 - Create user with complete data
    Given user reach the page
    When user enter username and password
    Then response status code shall contain 201
    And body contains Id


  Scenario: TC_02 - Get existing user
    Given user reach the page
    When user tries to get existing user
    Then response status code shall contain 200
    And response has proper format

  Scenario: TC_03 - Get not existing user
    Given user reach the page
    When user tries to get not existing user
    Then response status code shall contain 404
    And body is equal to '{}'

  Scenario: TC_04 - Get all users
    Given user reach the page
    When user tries to get all users
    Then response status code shall contain 200
    And response is list with 10 elements

  Scenario Outline: TC_05 - Check format of single user
    Given user reach the page
    When get data of single user with ID: <user ID>
    Then response status code is equal <response code>
    And  response body is validated for <response code>

    Examples:
    |user ID|response code|
    |1      |200          |
    |2      |200          |
    |13     |404          |
    |45465  |404          |

  Scenario Outline: TC_06 - Update user data
    Given user reach the page
    When update data of single user <id> <name> <username>
    Then response status code shall contain 200
    And body contains new data <name> <username>
    Examples:
    |name|username|id|
    |Brady|sagvdfs|1|
    |Auston|NoRingTill67|2|
    |Nathan|MissingEmptyNet|3|

  Scenario: TC_07 - Delete user
    Given user reach the page
    When delete single user
    Then response status code shall contain 200
    And body is equal to '{}'

  Scenario: TC_08 - Checking Content-Type response
    Given user reach the page
    When get data of existing user
    Then response status code shall contain 200
    And header is application/json

    Scenario: TC_09 - Creating user with minimal payload
      Given user reach the page
      When user is created with only name in payload
      Then response status code shall contain 201
      And body contains Id

      Scenario Outline: TC_10 - Checking nested fields
        Given user reach the page
        When user tries to get existing user
        Then response status code shall contain 200
        And <key> is nested in <field>

        Examples:
        |key| field|
        |city| address|
        |name| company|
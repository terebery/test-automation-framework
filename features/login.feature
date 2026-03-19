Feature: Login
  Scenario: Successful login
    Given user exists in the system
    When user sends login request
    Then response status code should be 200
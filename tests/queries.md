# Agent Test Queries

This document contains test queries used to evaluate the Community Analysis AI Agent.

## 1. Data Loading

**Query:** Load 6 posts about international students.

**Expected result:** The agent loads six sample posts about international students and confirms the number of posts loaded.

## 2. Network Graph Construction

**Query:** Build a network graph from the loaded posts.

**Expected result:** The agent builds a graph and reports the number of users and connections.

## 3. Community Detection

**Query:** Detect the communities in the network.

**Expected result:** The agent identifies connected user communities and reports their membership.

## 4. Community Identification

**Query:** How many communities were identified, and who are their members?

**Expected result:** The agent reports the number of communities and the members of each community.

## 5. Community Summary

**Query:** Summarize community 0.

**Expected result:** The agent provides the members, post count, and actual posts belonging to community 0.

## 6. Second Community Summary

**Query:** Summarize community 1.

**Expected result:** The agent provides the members, post count, and actual posts belonging to community 1.

## 7. Community Comparison

**Query:** Compare community 0 and community 1.

**Expected result:** The agent compares their members, post counts, and discussion content using available data.

## 8. Network Visualization

**Query:** Plot the network to visualize both communities.

**Expected result:** The agent generates a network visualization and saves it as `network.png`.

## 9. New Topic Analysis

**Query:** Load 3 posts about housing.

**Expected result:** The agent loads a new sample dataset and clears previous graph and community results.

## 10. Error Handling

**Query:** Build a network graph without loading any data first.

**Expected result:** The agent returns a meaningful error explaining that data must be loaded before building the graph.
# Photo-Album-Web-Application
Photo Alblum Web Application on AWS. Assignment3 @ COMS Cloud Computing and Big Data. Columbia

## Introduction

Our project implement a photo album web application, that can be searched using natural language through both text and voice. It use Lex, ElasticSearch, and Rekognition to create an intelligent search layer to query your photos for people, objects, actions, landmarks and more.

## Synopsis

This github repo contains frontend code and backend code which are respectively for two Code Pipelines. We use Code Pipeline for building and deploying our project. What's more, the AWS Cloud Formation template is used to represent all the infrastructure resources including Lambda, ElasticSearch, API Gateway, CodePipeline, etc. and permissions including IAM policies, roles, etc. For configuration files and template files, please look into buildspec.yml, cloudformation_template.yaml, samTemplate.yaml in the front-end/back-end folder.

## Team members

- Wenjie Chen `wc2685`: [email](mailto:wc2685@columbia.edu.com)
- Chong Hu `ch3467`: [email](mailto:ch3467@columbia.edu.com)
- Xinyue Wang `xw2647`
- Yuanmeng Xia `yx2548`

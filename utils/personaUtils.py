import requests
import json
import os
from datetime import datetime
from utils.extractKeywords import call_gemini

def generate_answers_from_profile(profileData, featuresData):
    try:
        # prompt = f"Generate answers from given profile data: {profileData}. Return only the answers, no explanations."
        response = generate_answer_for_feature(featuresData, profileData)
        return response
    except Exception as error:
        print(f'Error: {error}')
        return []
    
def generate_answer_for_feature(featuresData, profileData):
    # generic function to give output for every feature.
    # input: featureData and profileData
    # output: answer for the feature.
    # use the featureData and profileData to generate the answer.
    # return the answer.
    feature_answer = [];
    # global question, what job role does this person have on basis of its profile date, ask gemini to give answer.
    global_question = f"What job role does this person have on basis of its profile date: {profileData}? return only the answer, no explanations."
    answer_for_role = call_gemini(global_question)
    
    global_question_for_location = f"What is the current and usual location of this person on basis of its profile date: {profileData}? return only the answer, no explanations."
    answer_for_location = call_gemini(global_question_for_location)
    
    # for each feature, ask gemini to give answer.
    for feature in featuresData:
        
        # Check if there's explicit discussion of the feature in the profile data
        explicit_question = f"Is there any explicit discussion or mention of '{feature['description']}' with regards to {feature['options']} in the profile data: {profileData}? Answer only 'yes' or 'no', no explanations."
        has_explicit_info = call_gemini(explicit_question)
        
        # If there's explicit information, we'll prioritize that in our question
        if has_explicit_info.lower().strip() == "yes":
            question = f"Based on the EXPLICIT information in the profile data: {profileData}, what is the answer for the feature: {feature['description']}? Return only the answer from {feature['options']}, no explanations."
            answer = call_gemini(question)
            feature_answer.append(answer)
            break;
        
        question = f"What is the answer for the feature: {feature.description} on basis of its job role: {answer_for_role}, location: {answer_for_location} and profile data: {profileData}? return most probable answer from {feature['options']}, no explanations."
        answer = call_gemini(question)
        feature_answer.append(answer)

    return feature_answer

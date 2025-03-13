import requests
import json
import os
from datetime import datetime
import asyncio
from utils.extractKeywords import call_gemini

async def generate_answers_from_profile(profileData, featuresData):
    try:
        # Remove specified properties from profileData if they exist
        if isinstance(profileData, dict):
            # Remove top-level properties
            properties_to_remove = ['followers', 'connections', 'banner_image', 'description_html', 'certifications',
                                   'similar_profiles', 'people_also_viewed', 'avatar', 'activity', 'linkedin_num_id',
                                   'default_avatar', 'input', 'related_posts', 'comments', 'volunteer_experience']
            
            for prop in properties_to_remove:
                if prop in profileData:
                    del profileData[prop]
            
            # Clean experience array if it exists
            if 'experience' in profileData and isinstance(profileData['experience'], list):
                for experience in profileData['experience']:
                    remove_from_experience = ['description_html', 'company_logo_url',]
                    for prop in remove_from_experience:
                        if prop in experience:
                            del experience[prop]
                        
            if 'profile' in profileData:
                remove_from_profile = ['related_posts', 'comments']
                for prop in remove_from_profile:
                    if prop in profileData['profile']:
                        del profileData['profile'][prop]
                
        # print(f"Profile data: {profileData}\n\n")
        response = await generate_answer_for_feature(featuresData, profileData)
        return response
    except Exception as error:
        print(f'Error: {error}')
        return []
    
async def generate_answer_for_feature(featuresData, profileData):
    feature_answer = []
    # Get job role and location information first
    global_question = f"What job role does this person have on basis of its profile date: {profileData}? return only the answer, no explanations."
    answer_for_role = await call_gemini(global_question)
    # print(f"Answer for role: {answer_for_role}\n\n")
    global_question_for_location = f"What is the current and usual location of this person on basis of its profile date: {profileData}? return only the answer, no explanations."
    answer_for_location = await call_gemini(global_question_for_location)
    # print(f"Answer for location: {answer_for_location}\n\n")
    
    # Process features - could potentially be done in parallel
    for feature in featuresData:
        # print(f"Generating answer for features: {feature['description']}");
        explicit_question = f"Is there any explicit discussion or mention of '{feature.get('description')}' with regards to {feature.get('options')} in the profile data: {profileData}? Answer only 'yes' or 'no', no explanations."
        has_explicit_info = await call_gemini(explicit_question)
        
        if has_explicit_info.lower().strip() == "yes":
            question = f"Based on the EXPLICIT information in the profile data: {profileData}, what is the answer for the feature: {feature.get('description')}? Return only the answer from {feature.get('options')}, no explanations."
            answer = await call_gemini(question)
            feature_answer.append(answer)
            break
        
        question = f"What is the answer for the feature: {feature.get('description')} on basis of its job role: {answer_for_role}, location: {answer_for_location} and profile data: {profileData}? return most closest or probable answer from {feature.get('options')}, no explanations."
        answer = await call_gemini(question)
        res = {
            "feature": feature.get('description'),
            "answer": answer
        }
        feature_answer.append(res)

    return feature_answer
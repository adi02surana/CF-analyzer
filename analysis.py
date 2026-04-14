import pandas as pd
from utils import format_timestamp
from collections import defaultdict

def analyze_rating(rating_data):
    if not rating_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(rating_data)
    df['date'] = df['ratingUpdateTimeSeconds'].apply(format_timestamp)
    df['date'] = pd.to_datetime(df['date'])
    return df

def analyze_tags_and_weakness(status_data, handle):
    tag_stats = defaultdict(lambda: {'solved': 0, 'attempted': 0})
    problem_solved = set()
    
    for sub in status_data:
        problem = sub.get('problem', {})
        prob_id = f"{problem.get('contestId')}{problem.get('index')}"
        tags = problem.get('tags', [])
        verdict = sub.get('verdict')
        
        for tag in tags:
            tag_stats[tag]['attempted'] += 1
            if verdict == 'OK' and prob_id not in problem_solved:
                tag_stats[tag]['solved'] += 1
                
        if verdict == 'OK':
            problem_solved.add(prob_id)
            
    df = pd.DataFrame.from_dict(tag_stats, orient='index').reset_index()
    if df.empty:
        return df, [], []
        
    df.rename(columns={'index': 'tag'}, inplace=True)
    df['success_rate'] = df['solved'] / df['attempted']
    
    # Sort to find most and least solved
    df = df.sort_values(by='solved', ascending=False)
    
    median_solved = df['solved'].median()
    df['weakness_score'] = (1 - df['success_rate']) * 100 + (median_solved - df['solved']).clip(lower=0) * 2
    
    weak_topics = df.sort_values(by='weakness_score', ascending=False).head(3)['tag'].tolist()
    strong_topics = df.sort_values(by='solved', ascending=False).head(3)['tag'].tolist()
    
    return df, weak_topics, strong_topics

def analyze_difficulty(status_data):
    solved_problems = set()
    ratings = []
    
    for sub in status_data:
        if sub.get('verdict') == 'OK':
            problem = sub.get('problem', {})
            prob_id = f"{problem.get('contestId')}{problem.get('index')}"
            
            if prob_id not in solved_problems:
                solved_problems.add(prob_id)
                rating = problem.get('rating')
                if rating:
                    ratings.append(rating)
                    
    df = pd.DataFrame(ratings, columns=['rating'])
    return df

def analyze_activity(status_data):
    if not status_data:
        return pd.DataFrame()
        
    df = pd.DataFrame(status_data)
    df['date'] = df['creationTimeSeconds'].apply(format_timestamp)
    df['date'] = pd.to_datetime(df['date'])
    
    daily_subs = df.groupby('date').size().reset_index(name='submissions')
    return daily_subs

import sys
import matplotlib.pyplot as plt
from api import get_user_info, get_user_rating, get_user_status
from analysis import (
    analyze_rating, 
    analyze_tags_and_weakness, 
    analyze_difficulty, 
    analyze_activity
)
from visualization import (
    plot_rating_progression,
    plot_tag_distribution,
    plot_difficulty_histogram,
    plot_activity_heatmap
)
from utils import print_header, print_insight

def main():
    handle = input("Enter Codeforces Handle: ").strip()
    if not handle:
        print("Handle cannot be empty.")
        sys.exit(1)
        
    print(f"\n🔍 Fetching data for {handle}...")
    
    user_info = get_user_info(handle)
    if not user_info:
        print(f"Could not find user {handle}")
        sys.exit(1)
        
    rating_data = get_user_rating(handle)
    status_data = get_user_status(handle)
    
    print(f"✅ Data fetched successfully.\n")
    print(f"📊 Analyzing {len(status_data)} submissions...\n")
    
    df_rating = analyze_rating(rating_data)
    df_tags, weak_topics, strong_topics = analyze_tags_and_weakness(status_data, handle)
    df_diff = analyze_difficulty(status_data)
    df_activity = analyze_activity(status_data)
    
    print_header("PERFORMANCE INSIGHTS")
    
    if strong_topics:
        total_solved = df_tags['solved'].sum()
        top_tag = df_tags.iloc[0]
        pct = (top_tag['solved'] / total_solved) * 100 if total_solved > 0 else 0
        print_insight(f"Strongest area is '{strong_topics[0]}' ({pct:.1f}% of solved problems).")
        
    if weak_topics:
        print_insight(f"Identified weak areas: {', '.join(weak_topics)} (High attempt rate vs low success, or under-practiced).")
        
    if not df_diff.empty:
        # Determine the most common rating solved
        most_solved_rating = int(df_diff['rating'].mode()[0])
        print_insight(f"Most comfortable difficulty: {most_solved_rating} rating.")
        
        if weak_topics:
            print_insight(f"Recommendation: To improve, try solving problems in '{weak_topics[0]}' at {most_solved_rating + 100} rating.")
        
    if not df_activity.empty:
        recent_activity = df_activity.tail(30)
        active_days = len(recent_activity[recent_activity['submissions'] > 0])
        if active_days < 5:
            print_insight("Inconsistent practice in the last 30 days. Try solving 1-2 problems daily.")
        else:
            print_insight(f"Good consistency! Active {active_days} out of the last 30 days.")
            
    print_header("GENERATING VISUALIZATIONS")
    
    plot_rating_progression(df_rating, handle)
    plot_tag_distribution(df_tags, handle)
    plot_difficulty_histogram(df_diff, handle)
    plot_activity_heatmap(df_activity, handle)
    
    print("\n✅ Analysis complete! Opening graphs now...")
    print("ℹ️ Note: Close all graph windows to exit the program.")
    
    # This will block and directly open the graphs for the user until they are closed!
    plt.show()

if __name__ == "__main__":
    main()

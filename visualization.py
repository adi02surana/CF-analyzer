import matplotlib.pyplot as plt
import seaborn as sns
import os

def setup_plotting():
    try:
        sns.set_theme(style="darkgrid", palette="flare")
    except AttributeError:
        # Fallback for older seaborn
        sns.set(style="darkgrid", palette="flare")

def save_fig(plt_obj, filename):
    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    plt_obj.savefig(filepath, bbox_inches='tight', dpi=300)
    print(f"✅ Graph saved to: {filepath}")

def plot_rating_progression(df_rating, handle):
    if df_rating.empty:
        print("No rating data to plot.")
        return
        
    setup_plotting()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_rating, x='date', y='newRating', marker='o', linewidth=2)
    plt.title(f"Rating Progression for {handle}", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Rating", fontsize=12)
    plt.xticks(rotation=45)
    save_fig(plt, f"{handle}_rating_progression.png")
    
def plot_tag_distribution(df_tags, handle):
    if df_tags.empty:
        return
        
    setup_plotting()
    df_top = df_tags.head(15).copy()
    plt.figure(figsize=(12, 6))
    
    # Try using hue for seaborn >= 0.12.0 API requirements
    try:
        sns.barplot(data=df_top, x='solved', y='tag', hue='tag', legend=False, palette="viridis")
    except TypeError:
        sns.barplot(data=df_top, x='solved', y='tag', palette="viridis")
        
    plt.title(f"Most Solved Topics for {handle}", fontsize=14, fontweight='bold')
    plt.xlabel("Problems Solved", fontsize=12)
    plt.ylabel("Tag", fontsize=12)
    save_fig(plt, f"{handle}_tag_distribution.png")

def plot_difficulty_histogram(df_diff, handle):
    if df_diff.empty:
        return
        
    setup_plotting()
    plt.figure(figsize=(10, 5))
    bins = range(800, 3600, 100)
    sns.histplot(data=df_diff, x='rating', bins=bins, color="#e74c3c", kde=True)
    plt.title(f"Problem Difficulty Distribution for {handle}", fontsize=14, fontweight='bold')
    plt.xlabel("Problem Rating", fontsize=12)
    plt.ylabel("Problems Solved", fontsize=12)
    save_fig(plt, f"{handle}_difficulty_histogram.png")

def plot_activity_heatmap(df_activity, handle):
    if df_activity.empty:
        return
        
    setup_plotting()
    df_activity_recent = df_activity.tail(180).copy()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=df_activity_recent, x='date', y='submissions', color="#3498db", linewidth=2)
    plt.fill_between(df_activity_recent['date'], df_activity_recent['submissions'], color="#3498db", alpha=0.3)
    plt.title(f"Submission Activity (Last 180 Days) for {handle}", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Submissions", fontsize=12)
    plt.xticks(rotation=45)
    save_fig(plt, f"{handle}_activity.png")

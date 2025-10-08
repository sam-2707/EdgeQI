import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Generate response time data
np.random.seed(42)

# System load levels
load_levels = ['Light Load', 'Moderate Load', 'Heavy Load', 'Peak Load']

# Critical tasks response times (in milliseconds)
critical_tasks = {
    'Light Load': np.random.gamma(2, 50, 1000),  # Mean ~100ms
    'Moderate Load': np.random.gamma(2, 75, 1000),  # Mean ~150ms
    'Heavy Load': np.random.gamma(2, 125, 1000),  # Mean ~250ms
    'Peak Load': np.random.gamma(2, 175, 1000)   # Mean ~350ms
}

# Non-critical tasks response times (in milliseconds)
non_critical_tasks = {
    'Light Load': np.random.gamma(3, 100, 1000),   # Mean ~300ms
    'Moderate Load': np.random.gamma(3, 150, 1000), # Mean ~450ms
    'Heavy Load': np.random.gamma(3, 250, 1000),   # Mean ~750ms
    'Peak Load': np.random.gamma(3, 350, 1000)     # Mean ~1050ms
}

# Create subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('EDGE-QI Response Time Analysis Under Varying System Loads', fontsize=16, fontweight='bold')

# Colors for critical and non-critical tasks
critical_color = '#2E8B57'  # Sea Green
non_critical_color = '#CD853F'  # Peru

# Plot 1: Box plots for critical tasks
data_critical = [critical_tasks[load] for load in load_levels]
bp1 = ax1.boxplot(data_critical, labels=load_levels, patch_artist=True, 
                  boxprops=dict(facecolor=critical_color, alpha=0.7),
                  medianprops=dict(color='black', linewidth=2))
ax1.set_title('Critical Tasks Response Time Distribution', fontweight='bold')
ax1.set_ylabel('Response Time (ms)')
ax1.set_ylim(0, 800)
ax1.grid(True, alpha=0.3)

# Add 95th percentile line for critical tasks
percentiles_critical = [np.percentile(critical_tasks[load], 95) for load in load_levels]
ax1.plot(range(1, len(load_levels)+1), percentiles_critical, 'r--', linewidth=2, 
         marker='o', label='95th Percentile')
ax1.legend()

# Plot 2: Box plots for non-critical tasks
data_non_critical = [non_critical_tasks[load] for load in load_levels]
bp2 = ax2.boxplot(data_non_critical, labels=load_levels, patch_artist=True,
                  boxprops=dict(facecolor=non_critical_color, alpha=0.7),
                  medianprops=dict(color='black', linewidth=2))
ax2.set_title('Non-Critical Tasks Response Time Distribution', fontweight='bold')
ax2.set_ylabel('Response Time (ms)')
ax2.set_ylim(0, 2000)
ax2.grid(True, alpha=0.3)

# Add 95th percentile line for non-critical tasks
percentiles_non_critical = [np.percentile(non_critical_tasks[load], 95) for load in load_levels]
ax2.plot(range(1, len(load_levels)+1), percentiles_non_critical, 'r--', linewidth=2, 
         marker='o', label='95th Percentile')
ax2.legend()

# Plot 3: Mean response times comparison
mean_critical = [np.mean(critical_tasks[load]) for load in load_levels]
mean_non_critical = [np.mean(non_critical_tasks[load]) for load in load_levels]

x = np.arange(len(load_levels))
width = 0.35

bars1 = ax3.bar(x - width/2, mean_critical, width, label='Critical Tasks', 
                color=critical_color, alpha=0.7)
bars2 = ax3.bar(x + width/2, mean_non_critical, width, label='Non-Critical Tasks', 
                color=non_critical_color, alpha=0.7)

ax3.set_title('Mean Response Times by System Load', fontweight='bold')
ax3.set_ylabel('Mean Response Time (ms)')
ax3.set_xlabel('System Load Level')
ax3.set_xticks(x)
ax3.set_xticklabels(load_levels)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax3.annotate(f'{height:.0f}ms', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
for bar in bars2:
    height = bar.get_height()
    ax3.annotate(f'{height:.0f}ms', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

# Plot 4: Cumulative Distribution Function (CDF)
ax4.set_title('Response Time Cumulative Distribution (Heavy Load)', fontweight='bold')
ax4.set_xlabel('Response Time (ms)')
ax4.set_ylabel('Cumulative Probability')

# Plot CDF for heavy load scenario
critical_heavy = critical_tasks['Heavy Load']
non_critical_heavy = non_critical_tasks['Heavy Load']

# Sort data for CDF
critical_sorted = np.sort(critical_heavy)
non_critical_sorted = np.sort(non_critical_heavy)

# Calculate CDF
critical_cdf = np.arange(1, len(critical_sorted) + 1) / len(critical_sorted)
non_critical_cdf = np.arange(1, len(non_critical_sorted) + 1) / len(non_critical_sorted)

ax4.plot(critical_sorted, critical_cdf, label='Critical Tasks', color=critical_color, linewidth=2)
ax4.plot(non_critical_sorted, non_critical_cdf, label='Non-Critical Tasks', color=non_critical_color, linewidth=2)

# Add vertical lines for key percentiles
ax4.axvline(x=np.percentile(critical_heavy, 95), color=critical_color, linestyle='--', alpha=0.7)
ax4.axvline(x=np.percentile(non_critical_heavy, 95), color=non_critical_color, linestyle='--', alpha=0.7)
ax4.axhline(y=0.95, color='red', linestyle=':', alpha=0.5, label='95th Percentile')

ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 2000)

plt.tight_layout()
plt.savefig('response_times_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('response_times_analysis.pdf', bbox_inches='tight', facecolor='white')
plt.close()

# Generate summary statistics
print("Response Time Analysis Summary:")
print("=" * 50)
for load in load_levels:
    print(f"\n{load}:")
    print(f"  Critical Tasks - Mean: {np.mean(critical_tasks[load]):.1f}ms, 95th: {np.percentile(critical_tasks[load], 95):.1f}ms")
    print(f"  Non-Critical Tasks - Mean: {np.mean(non_critical_tasks[load]):.1f}ms, 95th: {np.percentile(non_critical_tasks[load], 95):.1f}ms")

print("\nResponse time analysis plots generated: response_times_analysis.png and response_times_analysis.pdf")
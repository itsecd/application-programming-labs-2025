import matplotlib.pyplot as plt


def create_brightness_plot(sorted_df, output_filename='brightness_range_sorted_plot.png'):
    """Создает график зависимости яркости от порядка в отсортированном списке."""
    plt.figure(figsize=(14, 8))
    
    plt.plot(
        range(len(sorted_df)), 
        sorted_df['brightness_range'], 
        marker='o', 
        linewidth=1.5, 
        markersize=3,
        color='blue',
        alpha=0.7,
        label='Диапазон яркости'
    )
    
    plt.xlabel('Порядковый номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Диапазон яркости (max-min)', fontsize=12)
    plt.title('Зависимость диапазона яркости от порядка в отсортированном списке', fontsize=14, fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    return output_filename
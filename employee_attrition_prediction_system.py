"""
Employee Attrition Prediction System Using Machine Learning
Predicts employee resignation risk using HR and workplace analytics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_employee_data(n_samples=1000, random_state=42):
    """Generate synthetic employee HR data"""
    np.random.seed(random_state)
    
    data = []
    
    for i in range(n_samples):
        # Generate employee features
        age = np.random.randint(22, 65)
        years_at_company = np.random.randint(0, 30)
        job_satisfaction = np.random.randint(1, 5)  # 1-4 scale
        monthly_salary = np.random.randint(1500, 15000)
        years_since_promotion = np.random.randint(0, 15)
        years_in_current_role = np.random.randint(0, 20)
        overtime_hours = np.random.randint(0, 100)
        attendance_percentage = np.random.uniform(70, 100)
        performance_rating = np.random.uniform(1, 5)
        work_life_balance = np.random.randint(1, 5)  # 1-4 scale
        department = np.random.choice(['Sales', 'IT', 'HR', 'Finance', 'Operations'])
        
        # Determine attrition based on features (realistic patterns)
        attrition_probability = 0.1  # Base probability
        
        if job_satisfaction <= 2:
            attrition_probability += 0.25
        if work_life_balance <= 2:
            attrition_probability += 0.15
        if years_since_promotion > 10:
            attrition_probability += 0.20
        if monthly_salary < 3000:
            attrition_probability += 0.15
        if overtime_hours > 60:
            attrition_probability += 0.10
        if performance_rating < 2:
            attrition_probability += 0.10
        if attendance_percentage < 80:
            attrition_probability += 0.15
        if years_at_company < 2:
            attrition_probability += 0.20
        
        # Cap probability
        attrition_probability = min(attrition_probability, 0.95)
        
        # Generate attrition label
        attrition = 1 if np.random.random() < attrition_probability else 0
        
        data.append({
            'Employee_ID': f'EMP{i+1:04d}',
            'Age': age,
            'Years_At_Company': years_at_company,
            'Job_Satisfaction': job_satisfaction,
            'Monthly_Salary': monthly_salary,
            'Years_Since_Promotion': years_since_promotion,
            'Years_In_Current_Role': years_in_current_role,
            'Overtime_Hours': overtime_hours,
            'Attendance_Percentage': attendance_percentage,
            'Performance_Rating': performance_rating,
            'Work_Life_Balance': work_life_balance,
            'Department': department,
            'Attrition': attrition
        })
    
    return pd.DataFrame(data)

def prepare_features(df):
    """Prepare features for modeling"""
    df_copy = df.copy()
    
    # Encode categorical variables
    le_dept = LabelEncoder()
    df_copy['Department_Encoded'] = le_dept.fit_transform(df_copy['Department'])
    
    # Select features for modeling
    feature_cols = ['Age', 'Years_At_Company', 'Job_Satisfaction', 'Monthly_Salary',
                   'Years_Since_Promotion', 'Years_In_Current_Role', 'Overtime_Hours',
                   'Attendance_Percentage', 'Performance_Rating', 'Work_Life_Balance',
                   'Department_Encoded']
    
    X = df_copy[feature_cols]
    y = df_copy['Attrition']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    
    return X_scaled, y, scaler, le_dept

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    models = {}
    results = []
    predictions = {}
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_proba_lr = lr.predict_proba(X_test)[:, 1]
    
    models['Logistic Regression'] = lr
    predictions['Logistic Regression'] = y_pred_lr
    results.append({
        'Model': 'Logistic Regression',
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr, zero_division=0),
        'Recall': recall_score(y_test, y_pred_lr, zero_division=0),
        'F1_Score': f1_score(y_test, y_pred_lr, zero_division=0),
        'ROC_AUC': roc_auc_score(y_test, y_proba_lr)
    })
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_proba_rf = rf.predict_proba(X_test)[:, 1]
    
    models['Random Forest'] = rf
    predictions['Random Forest'] = y_pred_rf
    results.append({
        'Model': 'Random Forest',
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf, zero_division=0),
        'Recall': recall_score(y_test, y_pred_rf, zero_division=0),
        'F1_Score': f1_score(y_test, y_pred_rf, zero_division=0),
        'ROC_AUC': roc_auc_score(y_test, y_proba_rf)
    })
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    y_proba_gb = gb.predict_proba(X_test)[:, 1]
    
    models['Gradient Boosting'] = gb
    predictions['Gradient Boosting'] = y_pred_gb
    results.append({
        'Model': 'Gradient Boosting',
        'Accuracy': accuracy_score(y_test, y_pred_gb),
        'Precision': precision_score(y_test, y_pred_gb, zero_division=0),
        'Recall': recall_score(y_test, y_pred_gb, zero_division=0),
        'F1_Score': f1_score(y_test, y_pred_gb, zero_division=0),
        'ROC_AUC': roc_auc_score(y_test, y_proba_gb)
    })
    
    return models, pd.DataFrame(results), predictions, y_test

def plot_attrition_distribution(df):
    """Plot attrition distribution and demographics"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Attrition distribution
    attrition_counts = df['Attrition'].value_counts()
    colors_attrition = ['#2ecc71', '#e74c3c']
    axes[0, 0].bar(['No Attrition', 'Attrition'], attrition_counts.values, color=colors_attrition, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 0].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Employee Attrition Distribution', fontsize=12, fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(attrition_counts.values):
        axes[0, 0].text(i, v + 5, str(v), ha='center', fontweight='bold')
    
    # Attrition by department
    dept_attrition = df.groupby('Department')['Attrition'].mean() * 100
    axes[0, 1].bar(dept_attrition.index, dept_attrition.values, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Attrition Rate by Department', fontsize=12, fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Age distribution by attrition
    df[df['Attrition'] == 0]['Age'].hist(bins=20, alpha=0.6, label='No Attrition', ax=axes[1, 0], color='#2ecc71', edgecolor='black')
    df[df['Attrition'] == 1]['Age'].hist(bins=20, alpha=0.6, label='Attrition', ax=axes[1, 0], color='#e74c3c', edgecolor='black')
    axes[1, 0].set_xlabel('Age', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Age Distribution by Attrition Status', fontsize=12, fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # Salary vs Job Satisfaction by attrition
    for attrition_status in [0, 1]:
        subset = df[df['Attrition'] == attrition_status]
        label = 'No Attrition' if attrition_status == 0 else 'Attrition'
        color = '#2ecc71' if attrition_status == 0 else '#e74c3c'
        axes[1, 1].scatter(subset['Monthly_Salary'], subset['Job_Satisfaction'], 
                          label=label, alpha=0.6, s=50, color=color, edgecolor='black', linewidth=0.5)
    axes[1, 1].set_xlabel('Monthly Salary', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Job Satisfaction', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Salary vs Job Satisfaction by Attrition', fontsize=12, fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/attrition_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: attrition_distribution.png")
    plt.close()

def plot_model_comparison(results_df):
    """Plot model performance comparison"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1_Score']
    
    for idx, metric in enumerate(metrics):
        row = idx // 2
        col = idx % 2
        
        axes[row, col].bar(results_df['Model'], results_df[metric], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[row, col].set_ylabel(metric, fontsize=11, fontweight='bold')
        axes[row, col].set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
        axes[row, col].set_ylim([0, 1.1])
        axes[row, col].grid(axis='y', alpha=0.3)
        axes[row, col].tick_params(axis='x', rotation=45)
        
        for i, v in enumerate(results_df[metric]):
            axes[row, col].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/attrition_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: attrition_model_comparison.png")
    plt.close()

def plot_confusion_matrices(models, X_test, y_test):
    """Plot confusion matrices"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for idx, (model_name, model) in enumerate(models.items()):
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], 
                   xticklabels=['No Attrition', 'Attrition'], 
                   yticklabels=['No Attrition', 'Attrition'], cbar=False)
        axes[idx].set_title(f'{model_name}\nConfusion Matrix', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('True Label', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/attrition_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: attrition_confusion_matrices.png")
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    feature_names = ['Age', 'Years_At_Company', 'Job_Satisfaction', 'Monthly_Salary',
                    'Years_Since_Promotion', 'Years_In_Current_Role', 'Overtime_Hours',
                    'Attendance_Percentage', 'Performance_Rating', 'Work_Life_Balance',
                    'Department']
    
    # Random Forest
    rf_model = models['Random Forest']
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1][:8]
    axes[0].barh(np.array(feature_names)[sorted_idx], importances[sorted_idx], color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest Feature Importance', fontsize=12, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb_model = models['Gradient Boosting']
    importances = gb_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1][:8]
    axes[1].barh(np.array(feature_names)[sorted_idx], importances[sorted_idx], color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting Feature Importance', fontsize=12, fontweight='bold')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/attrition_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: attrition_feature_importance.png")
    plt.close()

def plot_risk_analysis(df, models, X_scaled, y):
    """Plot attrition risk analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Job satisfaction impact
    js_attrition = df.groupby('Job_Satisfaction')['Attrition'].mean() * 100
    axes[0, 0].plot(js_attrition.index, js_attrition.values, marker='o', linewidth=2, markersize=8, color='#e74c3c')
    axes[0, 0].fill_between(js_attrition.index, js_attrition.values, alpha=0.3, color='#e74c3c')
    axes[0, 0].set_xlabel('Job Satisfaction Level', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Attrition Rate by Job Satisfaction', fontsize=12, fontweight='bold')
    axes[0, 0].grid(alpha=0.3)
    
    # Work-life balance impact
    wlb_attrition = df.groupby('Work_Life_Balance')['Attrition'].mean() * 100
    axes[0, 1].plot(wlb_attrition.index, wlb_attrition.values, marker='s', linewidth=2, markersize=8, color='#3498db')
    axes[0, 1].fill_between(wlb_attrition.index, wlb_attrition.values, alpha=0.3, color='#3498db')
    axes[0, 1].set_xlabel('Work-Life Balance Level', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Attrition Rate by Work-Life Balance', fontsize=12, fontweight='bold')
    axes[0, 1].grid(alpha=0.3)
    
    # Overtime impact
    overtime_bins = pd.cut(df['Overtime_Hours'], bins=5)
    overtime_attrition = df.groupby(overtime_bins)['Attrition'].mean() * 100
    axes[1, 0].bar(range(len(overtime_attrition)), overtime_attrition.values, color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_xlabel('Overtime Hours (Binned)', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Attrition Rate by Overtime Hours', fontsize=12, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Salary impact
    salary_bins = pd.cut(df['Monthly_Salary'], bins=5)
    salary_attrition = df.groupby(salary_bins)['Attrition'].mean() * 100
    axes[1, 1].bar(range(len(salary_attrition)), salary_attrition.values, color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 1].set_xlabel('Monthly Salary (Binned)', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Attrition Rate by Salary Range', fontsize=12, fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/attrition_risk_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: attrition_risk_analysis.png")
    plt.close()

def main():
    print("="*80)
    print("EMPLOYEE ATTRITION PREDICTION SYSTEM")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating employee HR data...")
    df = generate_employee_data(n_samples=1000)
    df.to_csv('/home/ubuntu/employee_attrition_data.csv', index=False)
    print(f"Dataset generated: {len(df)} employees")
    print(f"Attrition rate: {df['Attrition'].mean()*100:.2f}%")
    
    # Prepare features
    print("\n[2] Preparing features...")
    X, y, scaler, le_dept = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
    
    # Train models
    print("\n[3] Training classification models...")
    models, results_df, predictions, y_test = train_models(X_train, X_test, y_train, y_test)
    results_df.to_csv('/home/ubuntu/attrition_model_results.csv', index=False)
    print("\nModel Results:")
    print(results_df.to_string(index=False))
    
    # Generate visualizations
    print("\n[4] Generating visualizations...")
    plot_attrition_distribution(df)
    plot_model_comparison(results_df)
    plot_confusion_matrices(models, X_test, y_test)
    plot_feature_importance(models)
    plot_risk_analysis(df, models, X, y)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()

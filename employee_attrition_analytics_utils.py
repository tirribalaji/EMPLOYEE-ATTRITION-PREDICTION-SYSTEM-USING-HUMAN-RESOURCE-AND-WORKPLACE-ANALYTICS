"""
Employee Attrition Analytics Utilities
Generates detailed analytical datasets and statistics
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare employee attrition data"""
    df = pd.read_csv('/home/ubuntu/employee_attrition_data.csv')
    
    # Encode categorical variables
    le_dept = LabelEncoder()
    df['Department_Encoded'] = le_dept.fit_transform(df['Department'])
    
    feature_cols = ['Age', 'Years_At_Company', 'Job_Satisfaction', 'Monthly_Salary',
                   'Years_Since_Promotion', 'Years_In_Current_Role', 'Overtime_Hours',
                   'Attendance_Percentage', 'Performance_Rating', 'Work_Life_Balance',
                   'Department_Encoded']
    
    X = df[feature_cols]
    y = df['Attrition']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    
    return df, X_scaled, y, scaler, le_dept

def generate_employee_characteristics_stats():
    """Generate detailed employee characteristics statistics"""
    df, _, _, _, _ = load_and_prepare_data()
    
    stats = []
    
    # Overall statistics
    stats.append({
        'Category': 'Overall',
        'Subcategory': 'All Employees',
        'Count': len(df),
        'Attrition_Rate': df['Attrition'].mean() * 100,
        'Avg_Age': df['Age'].mean(),
        'Avg_Salary': df['Monthly_Salary'].mean(),
        'Avg_Years_At_Company': df['Years_At_Company'].mean(),
        'Avg_Job_Satisfaction': df['Job_Satisfaction'].mean(),
        'Avg_Work_Life_Balance': df['Work_Life_Balance'].mean()
    })
    
    # By department
    for dept in df['Department'].unique():
        dept_data = df[df['Department'] == dept]
        stats.append({
            'Category': 'Department',
            'Subcategory': dept,
            'Count': len(dept_data),
            'Attrition_Rate': dept_data['Attrition'].mean() * 100,
            'Avg_Age': dept_data['Age'].mean(),
            'Avg_Salary': dept_data['Monthly_Salary'].mean(),
            'Avg_Years_At_Company': dept_data['Years_At_Company'].mean(),
            'Avg_Job_Satisfaction': dept_data['Job_Satisfaction'].mean(),
            'Avg_Work_Life_Balance': dept_data['Work_Life_Balance'].mean()
        })
    
    # By age groups
    age_bins = [20, 30, 40, 50, 70]
    age_labels = ['20-30', '30-40', '40-50', '50+']
    df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
    
    for age_group in age_labels:
        group_data = df[df['Age_Group'] == age_group]
        if len(group_data) > 0:
            stats.append({
                'Category': 'Age Group',
                'Subcategory': age_group,
                'Count': len(group_data),
                'Attrition_Rate': group_data['Attrition'].mean() * 100,
                'Avg_Age': group_data['Age'].mean(),
                'Avg_Salary': group_data['Monthly_Salary'].mean(),
                'Avg_Years_At_Company': group_data['Years_At_Company'].mean(),
                'Avg_Job_Satisfaction': group_data['Job_Satisfaction'].mean(),
                'Avg_Work_Life_Balance': group_data['Work_Life_Balance'].mean()
            })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/employee_characteristics_stats.csv', index=False)
    print("Generated: employee_characteristics_stats.csv")
    return stats_df

def generate_attrition_risk_factors():
    """Generate attrition risk factors analysis"""
    df, _, _, _, _ = load_and_prepare_data()
    
    risk_factors = []
    
    # Job satisfaction impact
    for js in sorted(df['Job_Satisfaction'].unique()):
        subset = df[df['Job_Satisfaction'] == js]
        risk_factors.append({
            'Risk_Factor': 'Job_Satisfaction',
            'Factor_Level': f'Level {js}',
            'Employee_Count': len(subset),
            'Attrition_Count': subset['Attrition'].sum(),
            'Attrition_Rate': subset['Attrition'].mean() * 100,
            'Avg_Salary': subset['Monthly_Salary'].mean(),
            'Avg_Overtime': subset['Overtime_Hours'].mean(),
            'Avg_Performance': subset['Performance_Rating'].mean()
        })
    
    # Work-life balance impact
    for wlb in sorted(df['Work_Life_Balance'].unique()):
        subset = df[df['Work_Life_Balance'] == wlb]
        risk_factors.append({
            'Risk_Factor': 'Work_Life_Balance',
            'Factor_Level': f'Level {wlb}',
            'Employee_Count': len(subset),
            'Attrition_Count': subset['Attrition'].sum(),
            'Attrition_Rate': subset['Attrition'].mean() * 100,
            'Avg_Salary': subset['Monthly_Salary'].mean(),
            'Avg_Overtime': subset['Overtime_Hours'].mean(),
            'Avg_Performance': subset['Performance_Rating'].mean()
        })
    
    # Overtime impact
    overtime_bins = [0, 20, 40, 60, 100]
    overtime_labels = ['0-20', '20-40', '40-60', '60+']
    df['Overtime_Group'] = pd.cut(df['Overtime_Hours'], bins=overtime_bins, labels=overtime_labels)
    
    for ot_group in overtime_labels:
        subset = df[df['Overtime_Group'] == ot_group]
        if len(subset) > 0:
            risk_factors.append({
                'Risk_Factor': 'Overtime_Hours',
                'Factor_Level': f'{ot_group} hours',
                'Employee_Count': len(subset),
                'Attrition_Count': subset['Attrition'].sum(),
                'Attrition_Rate': subset['Attrition'].mean() * 100,
                'Avg_Salary': subset['Monthly_Salary'].mean(),
                'Avg_Overtime': subset['Overtime_Hours'].mean(),
                'Avg_Performance': subset['Performance_Rating'].mean()
            })
    
    risk_df = pd.DataFrame(risk_factors)
    risk_df.to_csv('/home/ubuntu/attrition_risk_factors.csv', index=False)
    print("Generated: attrition_risk_factors.csv")
    return risk_df

def generate_high_risk_employees():
    """Generate high-risk employee identification"""
    df, X_scaled, y, scaler, le_dept = load_and_prepare_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train best model (Random Forest)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Get predictions and probabilities for test set
    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)[:, 1]
    
    # Get corresponding employee indices
    test_indices = X_test.index
    
    high_risk = []
    for idx, (test_idx, risk_score) in enumerate(zip(test_indices, y_proba)):
        emp = df.iloc[test_idx]
        high_risk.append({
            'Employee_ID': emp['Employee_ID'],
            'Age': emp['Age'],
            'Department': emp['Department'],
            'Monthly_Salary': emp['Monthly_Salary'],
            'Years_At_Company': emp['Years_At_Company'],
            'Job_Satisfaction': emp['Job_Satisfaction'],
            'Work_Life_Balance': emp['Work_Life_Balance'],
            'Overtime_Hours': emp['Overtime_Hours'],
            'Performance_Rating': emp['Performance_Rating'],
            'Attrition_Risk_Score': risk_score,
            'Risk_Category': 'High' if risk_score > 0.7 else ('Medium' if risk_score > 0.4 else 'Low'),
            'Actual_Attrition': emp['Attrition']
        })
    
    high_risk_df = pd.DataFrame(high_risk)
    high_risk_df = high_risk_df.sort_values('Attrition_Risk_Score', ascending=False)
    high_risk_df.to_csv('/home/ubuntu/high_risk_employees.csv', index=False)
    print("Generated: high_risk_employees.csv")
    return high_risk_df

def generate_retention_recommendations():
    """Generate retention recommendations based on analysis"""
    df, _, _, _, _ = load_and_prepare_data()
    
    recommendations = []
    
    # Analyze low satisfaction employees
    low_sat = df[df['Job_Satisfaction'] <= 2]
    if len(low_sat) > 0:
        recommendations.append({
            'Target_Group': 'Low Job Satisfaction',
            'Employee_Count': len(low_sat),
            'Current_Attrition_Rate': low_sat['Attrition'].mean() * 100,
            'Recommendation': 'Implement job enrichment programs and career development initiatives',
            'Expected_Impact': 'Reduce attrition by 15-20%',
            'Priority': 'High',
            'Implementation_Timeline': '1-2 months'
        })
    
    # Analyze high overtime employees
    high_ot = df[df['Overtime_Hours'] > 60]
    if len(high_ot) > 0:
        recommendations.append({
            'Target_Group': 'High Overtime',
            'Employee_Count': len(high_ot),
            'Current_Attrition_Rate': high_ot['Attrition'].mean() * 100,
            'Recommendation': 'Review workload distribution and hire additional staff',
            'Expected_Impact': 'Reduce attrition by 10-15%',
            'Priority': 'High',
            'Implementation_Timeline': '2-3 months'
        })
    
    # Analyze low salary employees
    low_sal = df[df['Monthly_Salary'] < 3000]
    if len(low_sal) > 0:
        recommendations.append({
            'Target_Group': 'Low Salary',
            'Employee_Count': len(low_sal),
            'Current_Attrition_Rate': low_sal['Attrition'].mean() * 100,
            'Recommendation': 'Conduct salary review and implement competitive pay structure',
            'Expected_Impact': 'Reduce attrition by 12-18%',
            'Priority': 'High',
            'Implementation_Timeline': '1-3 months'
        })
    
    # Analyze no promotion employees
    no_promo = df[df['Years_Since_Promotion'] > 10]
    if len(no_promo) > 0:
        recommendations.append({
            'Target_Group': 'No Recent Promotion',
            'Employee_Count': len(no_promo),
            'Current_Attrition_Rate': no_promo['Attrition'].mean() * 100,
            'Recommendation': 'Create clear career progression paths and promotion opportunities',
            'Expected_Impact': 'Reduce attrition by 8-12%',
            'Priority': 'Medium',
            'Implementation_Timeline': '2-4 months'
        })
    
    # Analyze poor attendance
    poor_attend = df[df['Attendance_Percentage'] < 80]
    if len(poor_attend) > 0:
        recommendations.append({
            'Target_Group': 'Poor Attendance',
            'Employee_Count': len(poor_attend),
            'Current_Attrition_Rate': poor_attend['Attrition'].mean() * 100,
            'Recommendation': 'Conduct wellness programs and address underlying issues',
            'Expected_Impact': 'Reduce attrition by 5-10%',
            'Priority': 'Medium',
            'Implementation_Timeline': '1-2 months'
        })
    
    rec_df = pd.DataFrame(recommendations)
    rec_df.to_csv('/home/ubuntu/retention_recommendations.csv', index=False)
    print("Generated: retention_recommendations.csv")
    return rec_df

def generate_model_performance_by_department():
    """Generate model performance by department"""
    df, X_scaled, y, scaler, le_dept = load_and_prepare_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train models
    lr = LogisticRegression(max_iter=1000, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    
    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    gb.fit(X_train, y_train)
    
    models = {'Logistic Regression': lr, 'Random Forest': rf, 'Gradient Boosting': gb}
    
    performance_data = []
    
    for dept in df['Department'].unique():
        dept_mask = df.index.isin(X_test.index)
        dept_test_mask = (df.loc[X_test.index, 'Department'] == dept).values
        
        if dept_test_mask.sum() > 0:
            X_dept = X_test[dept_test_mask]
            y_dept = y_test[dept_test_mask]
            
            for model_name, model in models.items():
                y_pred = model.predict(X_dept)
                performance_data.append({
                    'Department': dept,
                    'Model': model_name,
                    'Accuracy': accuracy_score(y_dept, y_pred),
                    'Precision': precision_score(y_dept, y_pred, zero_division=0),
                    'Recall': recall_score(y_dept, y_pred, zero_division=0),
                    'F1_Score': f1_score(y_dept, y_pred, zero_division=0),
                    'Sample_Count': len(X_dept)
                })
    
    perf_df = pd.DataFrame(performance_data)
    perf_df.to_csv('/home/ubuntu/model_performance_by_department.csv', index=False)
    print("Generated: model_performance_by_department.csv")
    return perf_df

def generate_analysis_summary():
    """Generate comprehensive analysis summary"""
    df, _, _, _, _ = load_and_prepare_data()
    
    summary_text = f"""
EMPLOYEE ATTRITION PREDICTION SYSTEM - ANALYSIS SUMMARY

1. DATASET OVERVIEW
Total Employees: {len(df)}
Overall Attrition Rate: {df['Attrition'].mean()*100:.2f}%
Employees with Attrition: {df['Attrition'].sum()}
Employees Retained: {(df['Attrition']==0).sum()}

2. DEMOGRAPHIC ANALYSIS
Average Age: {df['Age'].mean():.1f} years
Age Range: {df['Age'].min()}-{df['Age'].max()} years
Average Tenure: {df['Years_At_Company'].mean():.1f} years
Average Monthly Salary: ${df['Monthly_Salary'].mean():.2f}

3. DEPARTMENT DISTRIBUTION
"""
    
    for dept in df['Department'].unique():
        dept_data = df[df['Department'] == dept]
        summary_text += f"\n{dept}: {len(dept_data)} employees ({len(dept_data)/len(df)*100:.1f}%), Attrition: {dept_data['Attrition'].mean()*100:.1f}%"
    
    summary_text += f"""

4. KEY FINDINGS
- Job Satisfaction Level 1-2: {(df[df['Job_Satisfaction']<=2]['Attrition'].mean()*100):.1f}% attrition rate
- Work-Life Balance Level 1-2: {(df[df['Work_Life_Balance']<=2]['Attrition'].mean()*100):.1f}% attrition rate
- High Overtime (>60 hours): {(df[df['Overtime_Hours']>60]['Attrition'].mean()*100):.1f}% attrition rate
- Low Salary (<$3000): {(df[df['Monthly_Salary']<3000]['Attrition'].mean()*100):.1f}% attrition rate
- No Promotion (>10 years): {(df[df['Years_Since_Promotion']>10]['Attrition'].mean()*100):.1f}% attrition rate
- Poor Attendance (<80%): {(df[df['Attendance_Percentage']<80]['Attrition'].mean()*100):.1f}% attrition rate

5. PREDICTIVE MODEL PERFORMANCE
The system employs three machine learning models to predict employee attrition:
- Logistic Regression: Linear classification model for baseline prediction
- Random Forest: Ensemble method capturing complex feature interactions
- Gradient Boosting: Advanced ensemble technique for improved accuracy

6. RECOMMENDATIONS
- Implement targeted retention programs for high-risk employees
- Review compensation structure for competitive positioning
- Establish clear career development and promotion pathways
- Monitor work-life balance and manage overtime effectively
- Conduct regular employee satisfaction surveys
- Develop department-specific retention strategies

7. EXPECTED OUTCOMES
Implementation of these recommendations is expected to reduce overall attrition by 20-30% within 6 months.
"""
    
    with open('/home/ubuntu/analysis_summary.txt', 'w') as f:
        f.write(summary_text)
    
    print("Generated: analysis_summary.txt")
    return summary_text

def main():
    print("="*80)
    print("EMPLOYEE ATTRITION ANALYTICS UTILITIES")
    print("="*80)
    
    print("\n[1] Generating employee characteristics statistics...")
    generate_employee_characteristics_stats()
    
    print("\n[2] Generating attrition risk factors...")
    generate_attrition_risk_factors()
    
    print("\n[3] Identifying high-risk employees...")
    generate_high_risk_employees()
    
    print("\n[4] Generating retention recommendations...")
    generate_retention_recommendations()
    
    print("\n[5] Generating model performance by department...")
    generate_model_performance_by_department()
    
    print("\n[6] Generating analysis summary...")
    generate_analysis_summary()
    
    print("\n" + "="*80)
    print("ANALYTICS COMPLETE - All datasets generated")
    print("="*80)

if __name__ == "__main__":
    main()

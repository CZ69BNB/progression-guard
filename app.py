import streamlit as st
import pandas as pd

st.set_page_config(page_title="ProgressionGuard", page_icon="🩺", layout="wide")

st.title("🩺 ProgressionGuard: Multi-Organ Silent Progression Engine")
st.caption("Cardiorenal-Metabolic Early Detection & Triage Decision Support System")

tab1, tab2, tab3 = st.tabs([
    "🧬 Cardiorenal Risk Profiler", 
    "📈 KDIGO Progression Matrix", 
    "🛡️ Organ-Protective Therapy Advisor"
])

# ==========================================
# TAB 1: CARDIORENAL RISK PROFILER
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("1. Patient Metabolic & Renal Panel")
        age = st.number_input("Age (Years)", min_value=18, max_value=90, value=56)
        gender = st.radio("Biological Sex", ["Male", "Female"], horizontal=True)
        
        st.markdown("**Lab Biomarkers:**")
        hba1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=16.0, value=8.2, step=0.1)
        sbp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=220, value=142)
        egfr = st.number_input("eGFR (mL/min/1.73m²)", min_value=5, max_value=140, value=52)
        uacr = st.number_input("Urine Albumin-to-Creatinine Ratio (UACR in mg/g)", min_value=1, max_value=5000, value=180)
        
        smoker = st.checkbox("Current Tobacco Smoker")
        prior_cvd = st.checkbox("Documented Prior ASCVD / Heart Failure")

    with col2:
        st.subheader("2. Multi-Organ Risk Synthesis")
        
        # KDIGO Risk Calculation
        if egfr >= 60 and uacr < 30:
            kdigo_risk = "Low Risk (Green)"
            risk_color = "success"
            dialysis_risk = "Low (<1% at 5 years)"
        elif (egfr >= 60 and 30 <= uacr <= 300) or (45 <= egfr < 60 and uacr < 30):
            kdigo_risk = "Moderate Risk (Yellow)"
            risk_color = "warning"
            dialysis_risk = "Moderate (1–5% at 5 years)"
        elif (egfr >= 60 and uacr > 300) or (45 <= egfr < 60 and 30 <= uacr <= 300) or (30 <= egfr < 45 and uacr < 30):
            kdigo_risk = "High Risk (Orange)"
            risk_color = "warning"
            dialysis_risk = "High (5–15% at 5 years)"
        else:
            kdigo_risk = "Very High Risk (Red)"
            risk_color = "error"
            dialysis_risk = "Critical (>15% at 5 years - Rapid Progression)"

        if risk_color == "success":
            st.success(f"**KDIGO Cardiorenal Staging:** {kdigo_risk}")
        elif risk_color == "warning":
            st.warning(f"**KDIGO Cardiorenal Staging:** {kdigo_risk}")
        else:
            st.error(f"**KDIGO Cardiorenal Staging:** {kdigo_risk}")

        st.markdown(f"""
        * **Projected Renal Deterioration Risk:** `{dialysis_risk}`
        * **Albuminuria Category:** `{"A1 (Normal <30 mg/g)" if uacr < 30 else "A2 (Microalbuminuria 30-300 mg/g)" if uacr <= 300 else "A3 (Severely Increased >300 mg/g)"}`
        * **eGFR Stage:** `{"G1 (>=90)" if egfr >= 90 else "G2 (60-89)" if egfr >= 60 else "G3a (45-59)" if egfr >= 45 else "G3b (30-44)" if egfr >= 30 else "G4 (15-29)" if egfr >= 15 else "G5 (Kidney Failure <15)"}`
        """)

        st.markdown("---")
        st.subheader("3. Immediate Clinical Directives")
        if uacr >= 30 or egfr < 60:
            st.markdown("🚨 **Silent Nephropathy Detected:** Patient exhibits objective signs of kidney damage without overt uremic symptoms.")
            st.markdown("- **Priority Action:** Initiate maximum tolerated dose of ACEi/ARB (e.g., Telmisartan) + SGLT2 inhibitor.")
        else:
            st.markdown("✅ **Normal Renal Biomarkers:** Maintain target glycemic control (HbA1c < 7.0%) and monitor UACR annually.")

# ==========================================
# TAB 2: KDIGO PROGRESSION MATRIX
# ==========================================
with tab2:
    st.subheader("📈 KDIGO 2024 CKD Heatmap & Prognosis Reference")
    st.caption("Composite risk of all-cause mortality, cardiovascular events, and progression to kidney failure.")

    matrix_data = pd.DataFrame({
        "eGFR Stage (mL/min)": ["G1 (>=90)", "G2 (60-89)", "G3a (45-59)", "G3b (30-44)", "G4 (15-29)", "G5 (<15)"],
        "A1: Normal (<30 mg/g)": ["🟢 Low", "🟢 Low", "🟡 Moderate", "🟠 High", "🔴 Very High", "🔴 Very High"],
        "A2: Microalbuminuria (30-300 mg/g)": ["🟡 Moderate", "🟡 Moderate", "🟠 High", "🔴 Very High", "🔴 Very High", "🔴 Very High"],
        "A3: Macroalbuminuria (>300 mg/g)": ["🟠 High", "🟠 High", "🔴 Very High", "🔴 Very High", "🔴 Very High", "🔴 Very High"]
    })
    st.dataframe(matrix_data, use_container_width=True)

    st.markdown("""
    **Stewardship Note on Silent Progression:**
    * Measuring **eGFR alone misses >60% of early kidney damage**. 
    * Spot **Urine ACR (UACR)** detects microalbuminuria years before serum creatinine rises or eGFR drops.
    """)

# ==========================================
# TAB 3: ORGAN-PROTECTIVE THERAPY ADVISOR
# ==========================================
with tab3:
    st.subheader("🛡️ Cardiorenal-Metabolic Pharmacotherapy Guard")
    st.caption("Evidence-based organ protection guidelines (ADA / KDIGO / ESC Standards)")

    st.markdown("### Pharmacotherapy Eligibility Check")

    # SGLT2i Check
    if egfr >= 20 and (uacr >= 30 or prior_cvd or hba1c >= 6.5):
        st.success("✅ **SGLT2 Inhibitor (e.g., Dapagliflozin 10mg OD / Empagliflozin 10mg OD):** Strongly Recommended (Cardiorenal protection & slowing CKD progression).")
    elif egfr < 20:
        st.warning("⚠️ **SGLT2 Inhibitor:** Initiation generally not recommended if eGFR < 20 mL/min/1.73m², but continued use permitted if previously tolerated.")

    # GLP-1 RA Check
    if hba1c >= 7.0 and (prior_cvd or egfr < 60 or uacr >= 30):
        st.success("✅ **GLP-1 Receptor Agonist (e.g., Dulaglutide / Semaglutide):** Recommended for glycemic control and major adverse cardiovascular event (MACE) reduction.")

    # High Intensity Statin Check
    if age >= 40 and (hba1c >= 6.5 or prior_cvd or egfr < 60):
        st.info("ℹ️ **Statin Therapy:** High-intensity statin (Atorvastatin 40-80mg or Rosuvastatin 20-40mg) indicated for primary/secondary ASCVD risk reduction.")

    st.markdown("---")
    st.subheader("4. Silent Microvascular Screening Reminders")
    st.checkbox("Annual Dilated Fundoscopic Eye Examination (Diabetic Retinopathy screen)")
    st.checkbox("10-Gram Semmes-Weinstein Monofilament Foot Examination (Diabetic Peripheral Neuropathy)")
    st.checkbox("Screen for Autonomic Neuropathy (Orthostatic Blood Pressure check)")

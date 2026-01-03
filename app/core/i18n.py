from typing import Dict

# Translation Dictionary
# Structure: key -> { 'en': '...', 'th': '...' }
TRANSLATIONS = {
    # --- Menu Items ---
    "menu_dashboard": {"en": "Dashboard", "th": "ภาพรวม"},
    "menu_work_orders": {"en": "Work Orders", "th": "ใบงาน"},
    "menu_teams": {"en": "Teams", "th": "ทีมช่าง"},
    "menu_users": {"en": "Users", "th": "ผู้ใช้งาน"},
    "menu_projects": {"en": "Projects", "th": "โครงการ"},
    "menu_calendar": {"en": "Calendar", "th": "ปฏิทิน"},
    "menu_reports": {"en": "Reports", "th": "รายงาน"},
    "menu_performance": {"en": "Performance", "th": "ประสิทธิภาพ"},

    # --- Common UI ---
    "search_placeholder": {"en": "Search Jobs...", "th": "ค้นหางาน..."},
    "btn_logout": {"en": "Logout", "th": "ออกจากระบบ"},
    "btn_profile": {"en": "Profile", "th": "ข้อมูลส่วนตัว"},
    "btn_save": {"en": "Save", "th": "บันทึก"},
    "btn_cancel": {"en": "Cancel", "th": "ยกเลิก"},
    "btn_edit": {"en": "Edit", "th": "แก้ไข"},
    "btn_delete": {"en": "Delete", "th": "ลบ"},
    "btn_view_all": {"en": "View All", "th": "ดูทั้งหมด"},
    "btn_add_new": {"en": "Add New", "th": "เพิ่มรายการใหม่"},
    "btn_close": {"en": "Close", "th": "ปิด"},
    "label_optional": {"en": "(Optional)", "th": "(ไม่บังคับ)"},
    "text_no_data": {"en": "No data found", "th": "ไม่พบข้อมูล"},

    # --- Dashboard ---
    "header_dashboard": {"en": "Today's Overview", "th": "ภาพรวมวันนี้"},
    "dash_pending_jobs": {"en": "Pending Jobs", "th": "งานรอดำเนินการ"},
    "dash_in_progress": {"en": "In Progress", "th": "กำลังดำเนินการ"},
    "dash_completed_today": {"en": "Completed Today", "th": "เสร็จสิ้นวันนี้"},
    "header_recent_jobs": {"en": "Recent & Urgent Jobs", "th": "งานล่าสุดและงานด่วน"},
    "col_technician": {"en": "Technician", "th": "ช่างผู้รับผิดชอบ"},
    
    # --- Jobs / Work Orders ---
    "job_header": {"en": "Work Orders", "th": "รายการใบงาน"},
    "btn_add_job": {"en": "Add New Job", "th": "สร้างใบงานใหม่"},
    "col_status": {"en": "Status", "th": "สถานะ"},
    "col_title": {"en": "Job Title", "th": "ชื่องาน"},
    "col_customer": {"en": "Customer", "th": "ลูกค้า"},
    "col_schedule": {"en": "Schedule", "th": "กำหนดการ"},
    "col_type": {"en": "Type", "th": "ประเภท"},
    "col_actions": {"en": "Actions", "th": "จัดการ"},
    "col_date": {"en": "Date", "th": "วันที่"},
    "label_unassigned": {"en": "Unassigned", "th": "ยังไม่มอบหมาย"},
    
    # --- Forms (Modal - Jobs) ---
    "modal_new_job": {"en": "New Job", "th": "สร้างใบงานใหม่"},
    "modal_edit_job": {"en": "Edit Job", "th": "แก้ไขใบงาน"},
    "label_title": {"en": "Title", "th": "หัวข้อ"},
    "label_description": {"en": "Description", "th": "รายละเอียด"},
    "label_project": {"en": "Project", "th": "โครงการ"},
    "label_type": {"en": "Type", "th": "ประเภทงาน"},
    "label_status": {"en": "Status", "th": "สถานะ"},
    "label_customer_name": {"en": "Customer Name", "th": "ชื่อลูกค้า"},
    "label_phone": {"en": "Phone", "th": "เบอร์โทร"},
    "label_address": {"en": "Address", "th": "ที่อยู่"},
    "label_date": {"en": "Date", "th": "วันที่"},
    "label_time": {"en": "Time", "th": "เวลา"},
    "label_location": {"en": "Location (Map)", "th": "พิกัดแผนที่"},
    "label_location": {"en": "Location (Map)", "th": "พิกัดแผนที่"},
    "label_assign": {"en": "Assign Technicians", "th": "มอบหมายช่าง"},
    "label_product_type": {"en": "Product Type", "th": "ประเภทสินค้า"},
    "label_model": {"en": "Model", "th": "รุ่น"},
    "label_serial": {"en": "Serial Number", "th": "หมายเลขเครื่อง"},
    "tab_details": {"en": "Details", "th": "รายละเอียด"},
    "tab_history": {"en": "History & Logs", "th": "ประวัติการทำงาน"},
    "btn_add_note": {"en": "Add Note", "th": "เพิ่มบันทึก"},
    "placeholder_note": {"en": "Enter note...", "th": "ระบุรายละเอียด..."},
    "header_history": {"en": "Job History", "th": "ประวัติการดำเนินงาน"},
    "btn_print": {"en": "Print Job Sheet", "th": "พิมพ์ใบงาน"},
    
    # --- Projects ---
    "proj_header": {"en": "Projects", "th": "โครงการทั้งหมด"},
    "btn_create_project": {"en": "Create Project", "th": "สร้างโครงการใหม่"},
    "modal_create_project": {"en": "Create Project", "th": "สร้างโครงการใหม่"},
    "modal_edit_project": {"en": "Edit Project", "th": "แก้ไขโครงการ"},
    "label_project_name": {"en": "Project Name", "th": "ชื่อโครงการ"},
    "label_start_date": {"en": "Start Date", "th": "วันที่เริ่ม"},
    "label_end_date": {"en": "End Date", "th": "วันที่สิ้นสุด"},
    "label_progress": {"en": "Progress", "th": "ความคืบหน้า"},
    "text_no_customer": {"en": "No Customer", "th": "ไม่ระบุลูกค้า"},
    "text_no_description": {"en": "No description", "th": "ไม่มีรายละเอียด"},
    "confirm_delete_project": {"en": "Delete this project?", "th": "ต้องการลบโครงการนี้ใช่หรือไม่?"},
    
    # --- Calendar ---
    "cal_header": {"en": "Schedule Calendar", "th": "ปฏิทินงาน"},
    "cal_today": {"en": "Today", "th": "วันนี้"},
    "cal_month": {"en": "Month", "th": "เดือน"},
    "cal_week": {"en": "Week", "th": "สัปดาห์"},
    "cal_day": {"en": "Day", "th": "วัน"},
    "modal_job_details": {"en": "Job Details", "th": "รายละเอียดงาน"},
    
    # --- Reports ---
    "rep_header": {"en": "Reports", "th": "รายงานผลการดำเนินงาน"},
    "btn_export_csv": {"en": "Export CSV", "th": "ส่งออก CSV"},
    "rep_total_jobs": {"en": "Total Jobs", "th": "งานทั้งหมด"},
    "rep_completed": {"en": "Completed", "th": "เสร็จสิ้น"},
    "rep_in_progress": {"en": "In Progress", "th": "กำลังทำ"},
    "rep_completion_rate": {"en": "Completion Rate", "th": "อัตราความสำเร็จ"},
    "chart_jobs_by_tech": {"en": "Jobs by Technician", "th": "งานแยกตามช่าง"},
    
    # --- Teams ---
    "team_header": {"en": "Team Management", "th": "จัดการทีมช่าง"},
    "btn_create_team": {"en": "Create New Team", "th": "สร้างทีมใหม่"},
    "col_color": {"en": "Color", "th": "สีประจำทีม"},
    "col_team_name": {"en": "Team Name", "th": "ชื่อทีม"},
    "col_members": {"en": "Members", "th": "จำนวนสมาชิก"},
    "modal_create_team": {"en": "Create Team", "th": "สร้างทีมใหม่"},
    "modal_edit_team": {"en": "Edit Team", "th": "แก้ไขทีม"},
    "label_team_name": {"en": "Team Name", "th": "ชื่อทีม"},
    "label_team_color": {"en": "Team Color", "th": "สีประจำทีม"},
    
    # --- Users ---
    "user_header": {"en": "User Management", "th": "จัดการผู้ใช้งาน"},
    "btn_add_user": {"en": "Add User", "th": "เพิ่มผู้ใช้งาน"},
    "col_name": {"en": "Name", "th": "ชื่อ-สกุล"},
    "col_role": {"en": "Role", "th": "ตำแหน่ง"},
    "col_contact": {"en": "Contact", "th": "ข้อมูลติดต่อ"},
    "col_telegram": {"en": "Telegram ID", "th": "Telegram ID"},
    "modal_add_user": {"en": "Add User", "th": "เพิ่มผู้ใช้งาน"},
    "modal_edit_user": {"en": "Edit User", "th": "แก้ไขข้อมูลผู้ใช้"},
    "label_username": {"en": "Username", "th": "ชื่อผู้ใช้ (Username)"},
    "label_fullname": {"en": "Full Name", "th": "ชื่อ-นามสกุล"},
    "label_password": {"en": "Password", "th": "รหัสผ่าน"},
    "label_role": {"en": "Role", "th": "ตำแหน่ง"},
    "label_team": {"en": "Team", "th": "ทีมสังกัด"},
    "label_email": {"en": "Email", "th": "อีเมล"},
    "confirm_delete_user": {"en": "Are you sure you want to delete this user?", "th": "ยืนยันการลบผู้ใช้งานรายนี้?"},
    
    # --- Performance ---
    "perf_header": {"en": "Performance Analytics", "th": "วิเคราะห์ประสิทธิภาพ"},
    "perf_subheader": {"en": "Overview for current month", "th": "ภาพรวมประจำเดือนนี้"},
    "kpi_active": {"en": "Pending/Active", "th": "รอ/กำลังทำ"},
    "kpi_techs": {"en": "Technicians", "th": "ช่างเทคนิค"},
    "chart_status_dist": {"en": "Job Status Distribution", "th": "สัดส่วนสถานะงาน"},
    "chart_job_types": {"en": "Job Types", "th": "ประเภทงาน"},
    "chart_daily_workload": {"en": "Daily Workload (Last 7 Days)", "th": "ภาระงานรายวัน (7 วันย้อนหลัง)"},
    "chart_tech_workload": {"en": "Technician Workload", "th": "ภาระงานของช่าง"},
    
    # --- Status Values ---
    "status_pending": {"en": "Pending", "th": "รอดำเนินการ"},
    "status_assigned": {"en": "Assigned", "th": "มอบหมายแล้ว"},
    "status_in_progress": {"en": "In Progress", "th": "กำลังทำ"},
    "status_completed": {"en": "Completed", "th": "เสร็จสิ้น"},
    "status_cancelled": {"en": "Cancelled", "th": "ยกเลิก"},
    "status_on_hold": {"en": "On Hold", "th": "ระงับชั่วคราว"},
    "status_active": {"en": "Active", "th": "ใช้งาน"},
    "status_inactive": {"en": "Inactive", "th": "ระงับใช้งาน"},

    # --- Profile ---
    "header_profile": {"en": "My Profile", "th": "ข้อมูลส่วนตัวของฉัน"},
    "label_new_password": {"en": "New Password (leave blank to keep current)", "th": "รหัสผ่านใหม่ (ว่างไว้หากไม่ต้องการเปลี่ยน)"},
    "label_confirm_password": {"en": "Confirm New Password", "th": "ยืนยันรหัสผ่านใหม่"},
    "alert_pwd_mismatch": {"en": "Passwords do not match!", "th": "รหัสผ่านไม่ตรงกัน!"},
    "alert_profile_updated": {"en": "Profile updated!", "th": "อัปเดตข้อมูลสำเร็จ!"},
    "alert_update_error": {"en": "Error updating profile", "th": "เกิดข้อผิดพลาดในการอัปเดต"},

    # --- Login ---
    "login_title": {"en": "Login - Pimtong WM", "th": "เข้าสู่ระบบ - พิมพ์ทอง WM"},
    "header_signin": {"en": "Sign in to your account", "th": "ลงชื่อเข้าใช้บัญชีของคุณ"},
    "btn_signin": {"en": "Sign in", "th": "เข้าสู่ระบบ"},
    "err_login_invalid": {"en": "Invalid username or password.", "th": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"},
    "err_generic": {"en": "An error occurred.", "th": "เกิดข้อผิดพลาด"},
    "err_app_error": {"en": "Application Error", "th": "ข้อผิดพลาดของแอปพลิเคชัน"},
    "err_error": {"en": "Error", "th": "ข้อผิดพลาด"},
    "err_delete_job": {"en": "Error deleting job", "th": "เกิดข้อผิดพลาดในการลบใบงาน"},
    "confirm_delete_job": {"en": "Delete this job?", "th": "ยืนยันการลบใบงานนี้?"},
}

DEFAULT_LANG = "th"

def get_translation(key: str, lang: str = DEFAULT_LANG) -> str:
    """Get translation for a key, falling back to EN if missing."""
    item = TRANSLATIONS.get(key)
    if not item:
        return key # Return key if not found
    
    return item.get(lang, item.get("en", key))

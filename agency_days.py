def processing_agency_days_and_hours(new_df): 
    day_2 = { 'mwf': 'monday, wednesday, friday',
            'tth': 'tuesday, thursday',
            'mon-fri': 'monday, tuesday, wednesday, thursday, friday',
            'mon - fri':'monday, tuesday, wednesday, thursday, friday',
            'mon-sat': 'monday, tuesday, wednesday, thursday, friday, saturday',
            'm-f': 'monday, tuesday, wednesday, thursday, friday',
            'sat-sun': 'saturday, sunday',
            'tue-thu': 'tuesday, wednesday, thursday',
            'monday-friday':'monday, tuesday, wednesday, thursday, friday',
            'monday-thursday':'monday, tuesday, wednesday, thursday',
            'm-th' : 'monday, tuesday, wednesday, thursday',
            'thur' : 'thursday'}
    def generate_day_combinations():
        # Full day names and their abbreviations
        days = {
            'monday': ['mon', 'm'],
            'tuesday': ['tues', 'tu', 't'],
            'wednesday': ['wed', 'we', 'w'],
            'thursday': ['thu', 'th','thur'],
            'friday': ['fri', 'fr', 'f'],
            'saturday': ['sat', 'sa', 's'],
            'sunday': ['sun', 'su']
        }
        # Add single-day mappings for abbreviations
        combinations = {}
    
        for full_day, abbrs in days.items():
            for abbr in abbrs:
                combinations[abbr] = full_day  # Map abbreviations directly
        day_2.update(combinations)
    
        # Function to get full day range
        def get_full_day_range(start_full, end_full):
            start_idx = list(days.keys()).index(start_full)
            end_idx = list(days.keys()).index(end_full)
            if start_idx == end_idx:
                return start_full
            return ', '.join(list(days.keys())[start_idx:end_idx + 1])
    
        # Create comprehensive mapping
        day_abbreviation_mapping = {}
        day_abbreviation_mapping.update(day_2)
        # Generate all possible day range combinations
        for start_full, start_abbrs in days.items():
            for end_full, end_abbrs in days.items():
                # Skip if start day comes after end day
                if list(days.keys()).index(start_full) > list(days.keys()).index(end_full):
                    continue
    
                # Get the full day range
                full_day_range = get_full_day_range(start_full, end_full)
    
                # Add full day range
                day_abbreviation_mapping[f"{start_full}-{end_full}"] = full_day_range
                day_abbreviation_mapping[f"{start_full} - {end_full}"] = full_day_range
                day_abbreviation_mapping[f"{start_full} to {end_full}"] = full_day_range
                
    
                # Add combinations of abbreviations
                for start_abbr in start_abbrs:
                    for end_abbr in end_abbrs:
                        combinations = [
                            f"{start_abbr}-{end_abbr}",
                            f"{start_abbr} - {end_abbr}",
                            f"{start_abbr} to {end_abbr}"
                            
                        ]
                        for combo in combinations:
                            day_abbreviation_mapping[combo] = full_day_range
    
                        # Add combinations for mix of single and abbreviated names
                        if start_abbr != start_full:
                            day_abbreviation_mapping[f"{start_abbr}-{end_full}"] = full_day_range
                            day_abbreviation_mapping[f"{start_abbr} - {end_full}"] = full_day_range
                            day_abbreviation_mapping[f"{start_abbr} to {end_full}"] = full_day_range
                            
                        if end_abbr != end_full:
                            day_abbreviation_mapping[f"{start_full}-{end_abbr}"] = full_day_range
                            day_abbreviation_mapping[f"{start_full} - {end_abbr}"] = full_day_range
                            day_abbreviation_mapping[f"{start_full} to {end_abbr}"] = full_day_range
                            
                
        
        
        return day_abbreviation_mapping
    
    
    # Generate the mapping
    day_abbreviation_mapping = generate_day_combinations()
    
    
    
    
    # Optional: Print or inspect the mapping
    #for key, value in day_abbreviation_mapping.items():
        #print(f"{key}: {value}")
    
    
    
    import pandas as pd
    import re
    import json
    
    # Load the data from the specified Excel file and sheet
    file_path = '/Users/rsiddiq2/Documents/FBCENC Test.xlsx'
    sheet1_data = pd.ExcelFile(file_path).parse('Sheet1')
    
    # Rename the columns for convenience (if necessary)
    sheet1_data.rename(columns=lambda x: x.strip(), inplace=True)  # Removing any leading/trailing whitespace
    
    # Update column names to match your actual file's columns
    agency_no_column = 'Parent Agency No.'
    agency_name_column = 'Agency_Name' if 'Agency_Name' in sheet1_data.columns else 'Agency Name'
    delivery_info_column = 'Delivery Info.' if 'Delivery Info.' in sheet1_data.columns else 'Delivery Information'
    
    # Function to normalize time format
    def normalize_time(hour, minute, am_pm,is_end_time=False):
        # If minutes are not provided, set them to "00"
        
        if not minute:
            minute = "00"
        # if am_pm:
        #     am_pm = am_pm.replace('.', '').lower() 
        if am_pm in ['a', 'p']:
            am_pm = f"{am_pm}m"
        '''
        # If AM/PM is not provided, default to "AM" for start times and "PM" for end times
        if not am_pm:
            am_pm = "am"  # Assuming AM for start times
        
        if not is_end_time and int(hour) >= 12 and int(hour) <=6 and am_pm == "am":
            am_pm = "pm"
       
        if is_end_time and am_pm == "am" and int(hour) >= 1 : 
            am_pm = "pm"
        '''
        if not am_pm:
            if int(hour) ==12:
                am_pm="pm"
            elif int(hour) >6 and int(hour)<12:
                am_pm="am"
            else:
                am_pm = "pm"
        # Return the time in the format "HH:MM AM/PM"
        return f"{hour}:{minute} {am_pm}"
        
    # Function to normalize the days and times
    def normalize_days_and_times(text):
        # Convert text to lowercase for consistent matching
        text = text.lower()
        
        text = re.sub(r'\.', '', text)
        for abbr, days in day_abbreviation_mapping.items():
            text = re.sub(r'\b' + re.escape(abbr) + r'\b', days, text)
    
        #Replace individual day abbreviations with full names
        day_mapping = {
            'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday',
            'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday',
            'm': 'monday', 'w': 'wednesday','t': 'tuesday', 'f': 'friday',
            'sa': 'saturday', 'su' : 'sunday','fr':'friday', 'th': 'thursday',
            'thur':'thursday',
            'thurs':'thursday','tues':'tuesday'
        }
        for short, full in day_mapping.items():
            text = re.sub(r'\b' + re.escape(short) + r'\b', full, text, flags=re.IGNORECASE)
    
        # Replace plural days like "Thursdays" with singular form "Thursday"
        text = re.sub(r'\b(.*?s)\b', lambda m: m.group(1)[:-1], text)
        
        # Normalize time ranges in the format "8-5 pm" or "8 am - 5 pm"
        text = re.sub(
            r'(\d{1,2}):(\d{2})(a|p)\s*-\s*(\d{1,2}):(\d{2})(a|p)',
            lambda m: f"{normalize_time(m.group(1), m.group(2), m.group(3))} - {normalize_time(m.group(4), m.group(5), m.group(6), is_end_time=True)}",
            text, flags=re.IGNORECASE
        )
    
        # Handle patterns like "6a-6p" (without minutes)
        text = re.sub(
            r'(\d{1,2})(a|p)\s*-\s*(\d{1,2})(a|p)',
            lambda m: f"{normalize_time(m.group(1), '00', m.group(2))} - {normalize_time(m.group(3), '00', m.group(4), is_end_time=True)}",
            text, flags=re.IGNORECASE
        )
    
        # Normalize time ranges like "8-5 pm" or "8 am - 5 pm"
        text = re.sub(
            r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*-\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?',
            lambda m: f"{normalize_time(m.group(1), m.group(2), m.group(3))} - {normalize_time(m.group(4), m.group(5), m.group(6), is_end_time=True)}",
            text, flags=re.IGNORECASE
        )
      
        return text
    
    # Apply the normalization function to the 'Delivery Info.' column
    sheet1_data['Normalized_Delivery_Info'] = sheet1_data[delivery_info_column].apply(normalize_days_and_times)
    
    def standardize_delivery_info(normalized_text):
        standardized_info = []
    
        # Define patterns for days, weeks, and times
        #day_pattern = r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
        day_pattern = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
        week_pattern = r"(\d+(?:st|nd|rd|th))\s*(?:week)?"
        time_pattern = r"(\d{1,2}:\d{2}\s*(?:AM|PM)?(?:\s*[-to]+\s*\d{1,2}:\d{2}\s*(?:AM|PM)?)?)"
    
        # Split the text into parts for analysis
        parts = re.split(r'[;,]|\band\b', normalized_text)
    
        current_days = []
        current_weeks = []
        start_time = "Unknown"
        end_time = "Unknown"
    
        # Iterate over each part to identify days, weeks, and times in sequence
        for part in parts:
            part = part.strip()
            #print(f"Processing part: {part}")  # Debugging statement to see the current part being processed
    
            # Extract weeks if mentioned
            weeks = re.findall(week_pattern, part, re.IGNORECASE)
            if weeks:
                current_weeks.extend(weeks)  # Append weeks instead of replacing
    
                
            # Extract days
            days = re.findall(day_pattern, part)
            if days:
                current_days.extend(days)
    
            # Extract times if present
            time_match = re.search(time_pattern, part, re.IGNORECASE)
            if time_match:
                time_str = time_match.group().strip()
                #print(standardized_info)
                # Handle time ranges
                if '-' in time_str or 'to' in time_str:
                    start_time, end_time = map(str.strip, re.split(r'-|to', time_str, flags=re.IGNORECASE))
                else:
                    start_time = time_str
                    end_time = time_str
                    
                # Assign the found times to all current days
                if current_days:
                    
                    for day in current_days:
                        standardized_info.append({
                            "Day": day,
                            "Opening_Hour": start_time,
                            "Closing_Hour": end_time,
                            "Week": current_weeks if current_weeks else ["1", "2", "3", "4"]
                        })
                    
                    # Reset the current_days and current_weeks since we have assigned the times
                    current_days = []
                    current_weeks = []
                    start_time = "Unknown"
                    end_time = "Unknown"
    
        # If there are remaining days without assigned times, add them with "Unknown"
        if current_days:
            for day in current_days:
                standardized_info.append({
                    "Day": day,
                    "Opening_Hour": "Unknown",
                    "Closing_Hour": "Unknown",
                    "Week": current_weeks if current_weeks else ["1", "2", "3", "4"]
                })
        
        return json.dumps(standardized_info, indent=2)
    
    # Apply standardization to the 'Normalized_Delivery_Info' column
    sheet1_data['Standardized_Delivery_Info'] = sheet1_data['Normalized_Delivery_Info'].apply(standardize_delivery_info)
    
    
    # Print out the standardized delivery info for verification
    #print(sheet1_data[['Parent Agency No.', 'Standardized_Delivery_Info']].head())
    
    import pandas as pd
    import re
    from datetime import datetime
    
    # Sample dataframe (Replace with your actual dataframe)
    
    
    # Function to standardize time format
    def format_time_column(time_str):
        """Standardize time to HH:MM AM/PM format with space before AM/PM."""
        if pd.isna(time_str) or time_str.strip() == "":
            return ""
    
        # Ensure there's a space before AM/PM
        time_str = re.sub(r'([apAP][mM])$', r' \1', time_str)  # Add space if missing
    
        try:
            # Try parsing with HH:MM format
            time_obj = datetime.strptime(time_str, '%I:%M %p')
        except ValueError:
            # If that fails, try parsing with HH format (no minutes)
            time_obj = datetime.strptime(time_str, '%I %p')
    
        # Return standardized format
        return time_obj.strftime('%I:%M %p')
    
    import pandas as pd
    import json
    import re
    
    # Function to adjust morning and afternoon slots
    def adjust_time_slots(opening_hour, closing_hour):
        # Initialize time slots
        morning_open = ""
        morning_close = ""
        afternoon_open = ""
        afternoon_close = ""
    
        # Check if closing time is 12:00 PM or earlier
        if closing_hour.lower() == '12:00 pm':
            closing_hour = '11:59 AM'
    
        # Check if it's morning or afternoon split
        if 'am' in opening_hour.lower() and 'pm' in closing_hour.lower():
            # Split between morning and afternoon
            morning_open = opening_hour
            morning_close = '11:59 AM'
            afternoon_open = '12:00 PM'
            afternoon_close = closing_hour
        elif 'am' in opening_hour.lower() and 'am' in closing_hour.lower():
            # Morning only
            morning_open = opening_hour
            morning_close = closing_hour
        elif 'pm' in opening_hour.lower() and 'pm' in closing_hour.lower():
            # Afternoon only
            afternoon_open = opening_hour
            afternoon_close = closing_hour
        elif 'pm' in opening_hour.lower() and 'am' in closing_hour.lower():
            # Wrap-around case, adjust to PM closing
            afternoon_open = opening_hour
            afternoon_close = '11:59 PM'
    
        # Final fix to prevent afternoon slots for 12:00 PM
        if afternoon_open == '12:00 PM' and afternoon_close == '11:59 AM':
            afternoon_open = ""
            afternoon_close = ""
        morning_open = format_time_column(morning_open)
        morning_close = format_time_column(morning_close)
        afternoon_open= format_time_column(afternoon_open)
        afternoon_close= format_time_column(afternoon_close)
        return morning_open, morning_close, afternoon_open, afternoon_close
    
    # Process JSON data with grouped weeks
    def process_json_in_column(df, json_column):
        new_rows = []
        for index, row in df.iterrows():
            try:
                # Parse JSON data
                json_data = json.loads(row[json_column])
                time_slot_map = {}
    
                # Process each JSON entry
                for entry in json_data:
                    day = entry["Day"]
                    opening_hour = entry.get("Opening_Hour", "")
                    closing_hour = entry.get("Closing_Hour", "")
                    weeks = entry.get("Week", [""])
    
                    # Convert weeks to numeric format
                    numeric_weeks = [int(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', week)) for week in weeks]
    
                    # Adjust time slots
                    morning_open, morning_close, afternoon_open, afternoon_close = adjust_time_slots(opening_hour, closing_hour)
    
                    # Create a unique key for each time slot
                    time_key = (day, opening_hour, closing_hour, 
                                morning_open, morning_close, 
                                afternoon_open, afternoon_close)
    
                    # Group weeks for identical time slots
                    if time_key in time_slot_map:
                        # Merge and remove duplicates
                        time_slot_map[time_key] = sorted(list(set(time_slot_map[time_key] + numeric_weeks)))
                    else:
                        time_slot_map[time_key] = numeric_weeks
    
                # Generate rows by combining weeks
                for time_key, weeks in time_slot_map.items():
                    new_row = {
                        "Agency_No": row["No."],
                        "Day_of_Week": time_key[0],
                        "Opening_Hour": time_key[1],
                        "Closing_Hour": time_key[2],
                        "Morning_Opening_Hour": time_key[3],
                        "Morning_Closing_Hour": time_key[4],
                        "Afternoon_Opening_Hour": time_key[5],
                        "Afternoon_Closing_Hour": time_key[6],
                        "Week": ', '.join(map(str, sorted(weeks)))  # Combine weeks into comma-separated format
                    }
                    new_rows.append(new_row)
    
            except Exception as e:
                print(f"Error processing row {index}: {e}")
        return pd.DataFrame(new_rows)
    
    # Apply the function
    expanded_df = process_json_in_column(sheet1_data, 'Standardized_Delivery_Info')
    expanded_df.drop('Opening_Hour', axis=1, inplace=True)
    expanded_df.drop('Closing_Hour', axis=1, inplace=True)

    return expanded_df
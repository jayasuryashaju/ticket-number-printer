from flask import Flask, render_template, request
from flask import send_from_directory

app = Flask(__name__)

COLORS = {
    "Red": "#ef4444",
    "Blue": "#3b82f6",
    "Green": "#22c55e",
    "Black": "#0f172a",
    "Pink": "#e86bcf",
    "Orange": "#f97316",
    "Purple": "#a855f7",
    "Teal": "#14b8a6",
    "Navy": "#1e3a8a",
    "Maroon": "#7f1d1d"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            start_nums = request.form.getlist('start_num[]')
            end_nums = request.form.getlist('end_num[]')
            font_colors = request.form.getlist('font_color[]')
            bg_colors = request.form.getlist('bg_color[]')

            all_tickets = []

            for i in range(len(start_nums)):
                # 1. Check for empty inputs
                if not start_nums[i] or not end_nums[i]:
                    return render_template('index.html', error="Please fill in all number fields.", colors=COLORS)

                # Convert string "0090" to integer 90
                start = int(start_nums[i])
                end = int(end_nums[i])
                f_color_name = font_colors[i]
                bg_color_name = bg_colors[i]

                # 2. VALIDATION: Check 4 Digits
                # Changed 0000 to 0 to prevent Python Syntax Error
                if not (0 <= start <= 9999) or not (0 <= end <= 9999):
                    return render_template('index.html', error=f"Error in Series {i+1}: Numbers must be exactly 4 digits (0000-9999).", colors=COLORS)

                # 3. VALIDATION: Check Logical Range
                if start > end:
                    return render_template('index.html', error=f"Error in Series {i+1}: Start number cannot be greater than End number.", colors=COLORS)

                # 4. VALIDATION: Max 100 per series
                count = end - start + 1
                if count > 100:
                    return render_template('index.html', error=f"Error in Series {i+1}: Maximum 100 tickets allowed per series. You asked for {count}.", colors=COLORS)

                # Color Logic
                font_hex = COLORS.get(f_color_name, "#ef4444")
                if bg_color_name == "None":
                    bg_hex = "#ffffff" # White for background
                    border_hex = "#000000" # Black for border
                else:
                    bg_hex = COLORS.get(bg_color_name, "#e86bcf")
                    border_hex = bg_hex

                # Generate Tickets
                for num in range(start, end + 1):
                    all_tickets.append({
                        # THE FIX: f"{num:04d}" forces it to be 4 digits with leading zeros
                        # Example: 90 becomes "0090", 5 becomes "0005"
                        "number": f"{num:04d}", 
                        "font_color": font_hex,
                        "bg_color": bg_hex,
                        "border_color": border_hex
                    })

            # Pagination (18 per page)
            chunks = [all_tickets[i:i + 18] for i in range(0, len(all_tickets), 18)]

            return render_template('print_view.html', pages=chunks)

        except ValueError:
            return render_template('index.html', error="Invalid input detected.", colors=COLORS)

    return render_template('index.html', colors=COLORS)

# Route to serve Service Worker and Manifest from root
@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
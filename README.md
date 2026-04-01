# Wopyflow AI – AI Marketing Toolkit

Wopyflow AI is a lightweight, frontend-only AI marketing toolkit designed for founders, marketers, and small businesses to analyze landing pages and convert content instantly.

## 🚀 Features

### 1. Landing Page Analyzer
- **Rule-based Scoring:** Analyzes H1 headlines (length & keywords), CTA visibility, trust signals (reviews/logos), and audience clarity.
- **Visual Feedback:** Color-coded conversion readiness score (Red/Orange/Green) with metric-specific progress bars.
- **Actionable Insights:** Generates 5 specific improvement suggestions based on page analysis.
- **CORS Support:** Uses a proxy to fetch content from external URLs.

### 2. PDF to Social Media Post Generator
- **Multi-Platform Output:** Generates posts for Instagram (Carousel & Single), Reels, Twitter (Thread), and LinkedIn.
- **AI Modifiers:** Customize the output tone (Professional, Engaging, Witty), length (Short/Detailed), and emoji usage.
- **PDF Parsing:** Uses `pdf.js` for client-side text extraction.
- **Regeneration:** Update posts instantly with different modifiers without re-uploading the file.

### 3. Lead Generation & SEO
- **Integrated Form:** Email capture for professional reports (compatible with Netlify/Formspree).
- **SEO Optimized:** Built-in metadata for improved search visibility.
- **SaaS UI:** Modern, responsive design built with Tailwind CSS.

## 🛠️ Tech Stack
- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
- **Libraries:** `pdf.js` (PDF parsing), `allorigins.win` (CORS Proxy)

## 📦 Installation & Deployment

### Local Development
1. Clone the repository.
2. Open `index.html` in your browser (or use a local server like `Live Server` in VS Code).

### Hostinger / WordPress Deployment
To integrate Wopyflow AI into a WordPress site hosted on Hostinger:

1. **Option A: Custom HTML Block (Recommended)**
   - Create a new Page in WordPress.
   - Add a "Custom HTML" block.
   - Paste the entire content of `index.html`.
   - Ensure you are using a Full Width template to avoid layout conflicts.

2. **Option B: Subdomain/Subfolder**
   - Upload the project files to a subfolder (e.g., `/wopyflow/`) via File Manager or FTP in Hostinger.
   - Access the tool directly at `yourdomain.com/wopyflow/`.

3. **Option C: WordPress Plugin (Advanced)**
   - Use a plugin like "Insert Headers and Footers" to add Tailwind/PDF.js scripts, and "Shortcoder" to embed the HTML body.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

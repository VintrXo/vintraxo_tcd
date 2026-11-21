// VintraXo login page: a brand panel beside Frappe's own login form (which is left untouched), the
// VintraXo logo, and an Arabic / English switch for visitors who are not signed in yet. Runs on /login only.
(function () {
	const TEXT = {
		ar: {
			title: "تعلّم وتطوّر مع فريقك",
			sub: "دورات ودروس ومعرفة الشركة في مكان واحد، بالعربية والإنجليزية.",
			points: ["أكثر من 40 دورة بأمثلة تعمل في المتصفح", "تابع تقدمك واحصل على شهادات", "سياسات الشركة وإجراءاتها في متناولك"],
			brand: "منصة التعلّم",
		},
		en: {
			title: "Learn and grow with your team",
			sub: "Courses, lessons and company knowledge in one place, in Arabic and English.",
			points: ["40+ courses with examples that run in your browser", "Track your progress and earn certificates", "Company policies and procedures at hand"],
			brand: "Learning platform",
		},
	};
	const ICONS = [
		'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5V21h16"/>',
		'<circle cx="12" cy="9" r="5"/><path d="M8.5 13.5 7 21l5-3 5 3-1.5-7.5"/>',
		'<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
	];
	const LOGO = "/assets/vintraxo_tcd/images/tcd_logo.svg";

	function el(tag, cls, text) {
		const e = document.createElement(tag);
		if (cls) e.className = cls;
		if (text) e.textContent = text;
		return e;
	}

	function setLanguage(lang) {
		document.cookie = "preferred_language=" + lang + "; path=/; max-age=31536000; SameSite=Lax";
		location.reload();
	}

	function init() {
		if (document.body.dataset.path !== "login") return;
		const content = document.querySelector(".page_content");
		if (!content || content.querySelector(".tcd-login-brand")) return;
		const lang = (document.documentElement.lang || "en").slice(0, 2) === "ar" ? "ar" : "en";
		const t = TEXT[lang];

		document.querySelectorAll(".app-logo").forEach((img) => (img.src = LOGO));

		const form = el("div", "tcd-login-form");
		const inner = el("div");
		while (content.firstChild) inner.appendChild(content.firstChild);
		form.appendChild(inner);

		const brand = el("aside", "tcd-login-brand");
		const top = el("div", "tcd-login-brand-top");
		const logo = el("div", "tcd-login-logo");
		const img = el("img");
		img.src = LOGO;
		img.alt = "";
		logo.append(img, el("span", "", "VintraXo"), el("span", "tcd-login-tag", "· " + t.brand));
		const switcher = el("div", "tcd-login-lang");
		switcher.setAttribute("role", "group");
		for (const [code, label] of [["ar", "العربية"], ["en", "English"]]) {
			const b = el("button", "", label);
			b.type = "button";
			b.lang = code;
			b.setAttribute("aria-pressed", String(code === lang));
			b.addEventListener("click", () => code !== lang && setLanguage(code));
			switcher.appendChild(b);
		}
		top.append(logo, switcher);

		const middle = el("div");
		middle.append(el("h1", "", t.title), el("p", "", t.sub));
		const points = el("ul", "tcd-login-points");
		t.points.forEach((text, i) => {
			const li = el("li");
			li.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + ICONS[i] + "</svg>";
			li.appendChild(el("span", "", text));
			points.appendChild(li);
		});
		middle.appendChild(points);

		const chips = el("div", "tcd-login-chips");
		chips.setAttribute("aria-hidden", "true");
		for (const name of ["Python", "SQL", "JavaScript", "React", "Marketing", "Odoo"]) chips.appendChild(el("span", "", name));

		brand.append(top, middle, chips);
		content.append(brand, form);
		document.body.classList.add("tcd-login");
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();

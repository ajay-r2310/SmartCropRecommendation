document.addEventListener("DOMContentLoaded", () => {
  initialiseLanguageSwitcher();

  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => nav.classList.toggle("is-open"));
  }

  const search = document.querySelector(".table-search");
  if (search) {
    search.addEventListener("input", () => {
      const term = search.value.toLowerCase();
      document.querySelectorAll("tbody tr").forEach((row) => {
        row.style.display = row.textContent.toLowerCase().includes(term) ? "" : "none";
      });
    });
  }
});

const translations = {
  en: {},
  ta: {
    dept: "தமிழ்நாடு அரசு டிஜிட்டல் வேளாண்மை தளம்",
    appName: "ஸ்மார்ட் பயிர் பரிந்துரை அமைப்பு",
    navHome: "முகப்பு",
    navRecommendation: "பரிந்துரை",
    navHistory: "வரலாறு",
    navAbout: "பற்றி",
    navContact: "தொடர்பு",
    footerIntro: "தமிழ்நாடு வேளாண்மைக்கான தெளிவான, தரவு சார்ந்த பயிர் திட்டமிடல் உதவி.",
    footerServices: "சேவைகள்",
    footerServicesList: "வானிலை நுண்ணறிவு<br>பயிர் பொருத்தம்<br>பரிந்துரை வரலாறு",
    footerSupport: "ஆதரவு",
    footerSupportList: "துறை உதவி மையம்<br>agri-support@example.tn.gov.in<br>சென்னை, தமிழ்நாடு",
    heroKicker: "தமிழ்நாடு வேளாண்மை நுண்ணறிவு",
    heroTitle: "வானிலை அடிப்படையிலான AI வழிகாட்டுதலுடன் சரியான பயிரை தேர்வு செய்யுங்கள்.",
    heroText: "மாவட்டம், மண் வகை, பருவம், நிலப்பரப்பு ஆகியவற்றை உள்ளிட்டு மகசூல், லாபம், விதைப்பு வழிகாட்டுதலுடன் பயிர் பரிந்துரையை பெறுங்கள்.",
    heroCta: "பரிந்துரையை தொடங்கு",
    recommendation: "பரிந்துரை",
    farmInput: "பண்ணை விவரங்கள்",
    location: "இடம்",
    selectDistrict: "மாவட்டத்தைத் தேர்வு செய்யவும்",
    soilType: "மண் வகை",
    selectSoil: "மண் வகையைத் தேர்வு செய்யவும்",
    season: "பருவம்",
    selectSeason: "பருவத்தைத் தேர்வு செய்யவும்",
    landArea: "நிலப்பரப்பு ஏக்கரில்",
    landPlaceholder: "உதாரணம்: 2.5",
    predictButton: "சிறந்த பயிரை கணிக்கவும்",
    loadingText: "வானிலை பெற்று பரிந்துரை உருவாக்கப்படுகிறது...",
    noticeTitle: "வேளாண்மை அறிவிப்பு",
    noticeText: "பரிந்துரைகள் வானிலை, மண், பருவம் மற்றும் பிராந்திய பயிர் முறைகளைப் பயன்படுத்துகின்றன. நில ஆய்வு, நீர் கிடைப்பது, உள்ளூர் வேளாண்மை அலுவலர் ஆலோசனையும் கருத்தில் கொள்ள வேண்டும்.",
    districts: "மாவட்டங்கள்",
    soilTypes: "மண் வகைகள்",
    crops: "பயிர்கள்",
    advisory: "ஆலோசனை",
    tipsTitle: "வேளாண்மை குறிப்புகள்",
    tipRainTitle: "மழையை கண்காணிக்கவும்",
    tipRainText: "எதிர்பார்க்கப்படும் மழை மற்றும் மண் ஈரப்பதத்தைப் பொருத்து பாசனம் மற்றும் விதைப்பை திட்டமிடுங்கள்.",
    tipSoilTitle: "மண்ணை பரிசோதிக்கவும்",
    tipSoilText: "முக்கிய பருவ பயிர் மாற்றங்களுக்கு முன் மண் ஊட்டச்சத்துகளை மதிப்பாய்வு செய்யுங்கள்.",
    tipMarketTitle: "சந்தையை கண்காணிக்கவும்",
    tipMarketText: "AI பரிந்துரைகளுடன் சந்தை விலை போக்குகளையும் தேவையையும் இணைத்து பாருங்கள்.",
    platformServices: "தள சேவைகள்",
    servicesTitle: "நம்பகமான பயிர் திட்டமிடலுக்காக உருவாக்கப்பட்டது",
    serviceWeather: "நேரடி வானிலை பெறுதல்",
    serviceMl: "இயந்திரக் கற்றல் பரிந்துரை",
    serviceProfit: "லாப மதிப்பீடு",
    serviceHistory: "MongoDB வரலாறு",
    resultGenerated: "பரிந்துரை உருவாக்கப்பட்டது",
    resultBestCrop: "இந்த இடத்திற்கு சிறந்த பயிர்",
    resultBasedOn: "தேர்ந்தெடுத்த மண், பருவம், நிலப்பரப்பு மற்றும் வானிலை மதிப்புகளின் அடிப்படையில்.",
    resultBasedOnPrefix: "அடிப்படையாகக் கொண்டது:",
    soilLower: "மண்",
    seasonLower: "பருவம்",
    acresLower: "ஏக்கர்",
    resultBasedOnSuffix: "மற்றும் வானிலை மதிப்புகள்.",
    recommendedCrop: "பரிந்துரைக்கப்பட்ட பயிர்",
    temperature: "வெப்பநிலை",
    humidity: "ஈரப்பதம்",
    rainfall: "மழைப்பொழிவு",
    expectedYield: "எதிர்பார்க்கப்படும் மகசூல்",
    estimatedProfit: "மதிப்பிடப்பட்ட லாபம்",
    sowingMonth: "சிறந்த விதைப்பு மாதம்",
    confidence: "நம்பகத்தன்மை",
    newRecommendation: "புதிய பரிந்துரை",
    viewHistory: "வரலாற்றைக் காண்க",
    predictionRecords: "பரிந்துரை பதிவுகள்",
    historyTitle: "பரிந்துரை வரலாறு",
    allCrops: "அனைத்து பயிர்கள்",
    allSeasons: "அனைத்து பருவங்கள்",
    apply: "பயன்படுத்து",
    exportCsv: "CSV ஏற்றுமதி",
    searchHistory: "வரலாற்றில் தேடுக",
    time: "நேரம்",
    soil: "மண்",
    crop: "பயிர்",
    yield: "மகசூல்",
    profit: "லாபம்",
    emptyHistory: "பரிந்துரை வரலாறு இல்லை. MongoDB Atlas அமைத்து ஒரு பரிந்துரையை உருவாக்கவும்.",
    aboutProject: "திட்டம் பற்றி",
    aboutTitle: "நடைமுறை வேளாண்மை திட்டமிடலுக்கான AI ஆதரவு",
    aboutTextOne: "இந்த தளம் மாவட்டம், மண் வகை, பருவம், நிலப்பரப்பு, நேரடி வானிலை தரவு மற்றும் Random Forest மாதிரியை இணைத்து தமிழ்நாடு விவசாய நிலைக்கு பொருத்தமான பயிரை பரிந்துரைக்கிறது.",
    aboutTextTwo: "பயிர் பொருத்தம், எதிர்பார்க்கப்படும் மகசூல், லாபம் மற்றும் விதைப்பு காலத்தை தெளிவான டிஜிட்டல் சேவை வழியாக ஒப்பிட உதவுகிறது.",
    techFoundation: "தொழில்நுட்ப அடித்தளம்",
    techModel: "Scikit-learn Random Forest மாதிரி",
    techWeather: "OpenWeatherMap வானிலை சேவை",
    techDb: "MongoDB Atlas பரிந்துரை வரலாறு",
    techSecurity: "சரிபார்க்கப்பட்ட உள்ளீடுகள் மற்றும் சூழல் அடிப்படையிலான அமைப்பு",
    contact: "தொடர்பு",
    supportDesk: "வேளாண்மை ஆதரவு மையம்",
    name: "பெயர்",
    email: "மின்னஞ்சல்",
    district: "மாவட்டம்",
    message: "செய்தி",
    sendMessage: "செய்தி அனுப்பு",
    office: "அலுவலகம்",
    officeAddress: "வேளாண்மை மற்றும் விவசாயிகள் நலத்துறை, சென்னை, தமிழ்நாடு",
    faq: "அடிக்கடி கேட்கப்படும் கேள்விகள்",
    faqText: "அமைக்கப்பட்டிருந்தால் வானிலை மதிப்புகள் OpenWeatherMap இலிருந்து வரும். MongoDB Atlas இணைக்கப்பட்ட பிறகு பரிந்துரை வரலாறு தெரியும்.",
    notFoundTitle: "பக்கம் கிடைக்கவில்லை",
    notFoundText: "கோரிய வேளாண்மை சேவை பக்கம் கிடைக்கவில்லை.",
    serverErrorTitle: "சேவை தற்காலிகமாக கிடைக்கவில்லை",
    serverErrorText: "சில நிமிடங்களுக்குப் பிறகு மீண்டும் முயற்சிக்கவும்.",
    returnHome: "முகப்புக்கு திரும்பு",
  },
};

const valueTranslations = {
  ta: {
    district: {
      Ariyalur: "அரியலூர்",
      Chengalpattu: "செங்கல்பட்டு",
      Chennai: "சென்னை",
      Coimbatore: "கோயம்புத்தூர்",
      Cuddalore: "கடலூர்",
      Dharmapuri: "தர்மபுரி",
      Dindigul: "திண்டுக்கல்",
      Erode: "ஈரோடு",
      Kallakurichi: "கள்ளக்குறிச்சி",
      Kanchipuram: "காஞ்சிபுரம்",
      Kanniyakumari: "கன்னியாகுமரி",
      Karur: "கரூர்",
      Krishnagiri: "கிருஷ்ணகிரி",
      Madurai: "மதுரை",
      Mayiladuthurai: "மயிலாடுதுறை",
      Nagapattinam: "நாகப்பட்டினம்",
      Namakkal: "நாமக்கல்",
      Nilgiris: "நீலகிரி",
      Perambalur: "பெரம்பலூர்",
      Pudukkottai: "புதுக்கோட்டை",
      Ramanathapuram: "ராமநாதபுரம்",
      Ranipet: "ராணிப்பேட்டை",
      Salem: "சேலம்",
      Sivaganga: "சிவகங்கை",
      Tenkasi: "தென்காசி",
      Thanjavur: "தஞ்சாவூர்",
      Theni: "தேனி",
      Thoothukudi: "தூத்துக்குடி",
      Tiruchirappalli: "திருச்சிராப்பள்ளி",
      Tirunelveli: "திருநெல்வேலி",
      Tirupathur: "திருப்பத்தூர்",
      Tiruppur: "திருப்பூர்",
      Tiruvallur: "திருவள்ளூர்",
      Tiruvannamalai: "திருவண்ணாமலை",
      Tiruvarur: "திருவாரூர்",
      Vellore: "வேலூர்",
      Viluppuram: "விழுப்புரம்",
      Virudhunagar: "விருதுநகர்",
    },
    soil: {
      Alluvial: "வண்டல் மண்",
      Black: "கருப்பு மண்",
      Red: "சிவப்பு மண்",
      Laterite: "லேட்டரைட் மண்",
      Sandy: "மணற்பாங்கான மண்",
      Clay: "களிமண்",
      Loamy: "லோமி மண்",
    },
    season: {
      Kharif: "காரிஃப்",
      Rabi: "ரபி",
      Zaid: "சைத்",
      Summer: "கோடை",
      Winter: "குளிர்காலம்",
      Monsoon: "மழைக்காலம்",
    },
    crop: {
      Banana: "வாழை",
      Cotton: "பருத்தி",
      Groundnut: "நிலக்கடலை",
      Maize: "மக்காச்சோளம்",
      Millets: "சிறுதானியங்கள்",
      Pulses: "பயறு வகைகள்",
      Rice: "நெல்",
      Sugarcane: "கரும்பு",
      Turmeric: "மஞ்சள்",
      Vegetables: "காய்கறிகள்",
    },
    month: {
      January: "ஜனவரி",
      February: "பிப்ரவரி",
      March: "மார்ச்",
      April: "ஏப்ரல்",
      May: "மே",
      June: "ஜூன்",
      July: "ஜூலை",
      August: "ஆகஸ்ட்",
      September: "செப்டம்பர்",
      October: "அக்டோபர்",
      November: "நவம்பர்",
      December: "டிசம்பர்",
    },
  },
};

function initialiseLanguageSwitcher() {
  const savedLanguage = localStorage.getItem("smartCropLanguage") || "en";
  applyLanguage(savedLanguage);

  document.querySelectorAll(".language-button").forEach((button) => {
    button.addEventListener("click", () => {
      const language = button.dataset.lang || "en";
      localStorage.setItem("smartCropLanguage", language);
      applyLanguage(language);
    });
  });
}

function applyLanguage(language) {
  const dictionary = translations[language] || translations.en;
  document.documentElement.lang = language === "ta" ? "ta" : "en";

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (language === "en") {
      if (element.dataset.originalText) element.textContent = element.dataset.originalText;
      return;
    }
    if (!element.dataset.originalText) element.dataset.originalText = element.textContent;
    if (dictionary[key]) element.textContent = dictionary[key];
  });

  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    const key = element.dataset.i18nHtml;
    if (language === "en") {
      if (element.dataset.originalHtml) element.innerHTML = element.dataset.originalHtml;
      return;
    }
    if (!element.dataset.originalHtml) element.dataset.originalHtml = element.innerHTML;
    if (dictionary[key]) element.innerHTML = dictionary[key];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    if (language === "en") {
      if (element.dataset.originalPlaceholder) element.placeholder = element.dataset.originalPlaceholder;
      return;
    }
    if (!element.dataset.originalPlaceholder) element.dataset.originalPlaceholder = element.placeholder;
    if (dictionary[key]) element.placeholder = dictionary[key];
  });

  translateDynamicValues(language);

  document.querySelectorAll(".language-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.lang === language);
  });
}

function translateDynamicValues(language) {
  document.querySelectorAll("[data-translate-value]").forEach((element) => {
    if (!element.dataset.originalValueText) {
      element.dataset.originalValueText = element.textContent.trim();
    }

    const originalText = element.dataset.originalValueText;
    if (language === "en") {
      element.textContent = originalText;
      return;
    }

    const group = element.dataset.translateValue;
    const translatedValue = valueTranslations[language]?.[group]?.[originalText];
    element.textContent = translatedValue || originalText;
  });
}

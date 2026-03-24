// ===== GET ELEMENTS =====
const searchInput = document.getElementById("searchInput");
const locationFilter = document.getElementById("locationFilter");
const companies = document.querySelectorAll(".company-item");
const noResult = document.getElementById("noResult");

// ===== FILTER FUNCTION =====
function filterCompanies() {

    const searchValue = searchInput.value.toLowerCase();
    const locationValue = locationFilter.value;

    let visibleCount = 0;

    companies.forEach(company => {

        const name = company.getAttribute("data-name");
        const location = company.getAttribute("data-location");

        // CHECK MATCH
        const matchesSearch = name.includes(searchValue);
        const matchesLocation = locationValue === "" || location === locationValue;

        if (matchesSearch && matchesLocation) {
            company.style.display = "block";
            visibleCount++;
        } else {
            company.style.display = "none";
        }

    });

    // SHOW / HIDE EMPTY STATE
    if (visibleCount === 0) {
        noResult.style.display = "block";
    } else {
        noResult.style.display = "none";
    }
}

// ===== EVENTS =====
searchInput.addEventListener("keyup", filterCompanies);
locationFilter.addEventListener("change", filterCompanies);

// ===== OPTIONAL: SEARCH BUTTON CLICK =====
const searchBtn = document.querySelector(".search-btn");

if (searchBtn) {
    searchBtn.addEventListener("click", filterCompanies);
}
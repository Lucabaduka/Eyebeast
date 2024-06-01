// Eyebeast search function
const form = document.querySelector("search-box");
form?.addEventListener("submit", (e) => {
    e.preventDefault();

    // Collect Data
    const formData = new FormData(form);
    const searchTerm = formData.get("region")?.toString();

    // Clean Data
    let stripNS = searchTerm.replace("https://www.nationstates.net/region=", "");
    let cleanTerm = stripNS.toLowerCase().replace(/ /g, "_");
    let bleachedTerm = cleanTerm.replace(/[^a-z A-Z 0-9-_]+/g, "");

    // Transfer Data
    const url = new URL("/", window.location.origin);
    url.searchParams.set("region", bleachedTerm)
    window.location.assign(url.toString());
});
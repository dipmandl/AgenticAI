const STORAGE_KEY = "releaseNotesDashboard.releases";

const releaseForm = document.getElementById("release-form");
const releaseList = document.getElementById("release-list");
const template = document.getElementById("release-card-template");
const productFilterInput = document.getElementById("product-filter");
const searchFilterInput = document.getElementById("search-filter");
const breakingFilterSelect = document.getElementById("breaking-filter");
const submitButton = document.getElementById("submit-button");
const cancelEditButton = document.getElementById("cancel-edit-button");
const exportCsvButton = document.getElementById("export-csv-button");
const importJsonButton = document.getElementById("import-json-button");
const importJsonFileInput = document.getElementById("import-json-file");
const transferStatus = document.getElementById("transfer-status");
const teamNameInput = document.getElementById("teamName");
const teamNameError = document.getElementById("team-name-error");

let releases = loadReleases();
let editingReleaseId = null;

renderReleaseList();

releaseForm.addEventListener("submit", (event) => {
  event.preventDefault();
  clearTeamNameError();

  const formData = new FormData(releaseForm);
  const payload = {
    product: String(formData.get("product") || "").trim(),
    version: String(formData.get("version") || "").trim(),
    teamName: String(formData.get("teamName") || "").trim(),
    title: String(formData.get("title") || "").trim(),
    description: String(formData.get("description") || "").trim(),
    releaseDate: String(formData.get("releaseDate") || ""),
    isBreaking: formData.get("breaking") === "on"
  };

  if (!payload.teamName) {
    showTeamNameError("Team name is required.");
    teamNameInput.focus();
    return;
  }

  if (!payload.product || !payload.version || !payload.title || !payload.description || !payload.releaseDate) {
    return;
  }

  if (editingReleaseId) {
    releases = releases.map((release) => {
      if (release.id !== editingReleaseId) {
        return release;
      }

      return {
        ...release,
        ...payload
      };
    });
    resetEditMode();
  } else {
    releases.unshift({
      id: generateId(),
      ...payload
    });
    releaseForm.reset();
  }

  saveReleases(releases);
  renderReleaseList();
});

productFilterInput.addEventListener("change", renderReleaseList);
searchFilterInput.addEventListener("input", renderReleaseList);
breakingFilterSelect.addEventListener("change", renderReleaseList);
cancelEditButton.addEventListener("click", resetEditMode);
exportCsvButton.addEventListener("click", exportReleasesCsv);
importJsonButton.addEventListener("click", () => {
  importJsonFileInput.click();
});
teamNameInput.addEventListener("input", () => {
  if (teamNameInput.value.trim()) {
    clearTeamNameError();
  }
});
importJsonFileInput.addEventListener("change", (event) => {
  const selectedFile = event.target.files && event.target.files[0];
  if (!selectedFile) {
    return;
  }

  importReleasesFromFile(selectedFile);
  importJsonFileInput.value = "";
});

function loadReleases() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return seedData();
  }

  try {
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed;
    }
  } catch {
    return seedData();
  }

  return seedData();
}

function saveReleases(items) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function renderReleaseList() {
  updateProductFilterOptions();
  const filtered = getFilteredReleases();

  releaseList.innerHTML = "";

  if (filtered.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No release notes match your current filters.";
    releaseList.appendChild(empty);
    return;
  }

  for (const release of filtered) {
    const card = template.content.firstElementChild.cloneNode(true);
    card.classList.toggle("breaking", release.isBreaking);

    card.querySelector(".product-version").textContent = `${release.product} - ${release.version}`;
    card.querySelector(".release-title").textContent = release.title;
    card.querySelector(".release-team").textContent = `Team: ${getDisplayTeamName(release)}`;
    card.querySelector(".release-description").textContent = release.description;
    card.querySelector(".release-date").textContent = `Release date: ${formatDate(release.releaseDate)}`;

    const badge = card.querySelector(".badge");
    badge.textContent = release.isBreaking ? "Breaking Change" : "Non-Breaking";
    badge.classList.add(release.isBreaking ? "breaking" : "safe");

    const editButton = card.querySelector(".edit-btn");
    editButton.addEventListener("click", () => {
      startEdit(release.id);
    });

    const deleteButton = card.querySelector(".delete-btn");
    deleteButton.addEventListener("click", () => {
      deleteRelease(release.id);
    });

    releaseList.appendChild(card);
  }
}

function startEdit(id) {
  const release = releases.find((item) => item.id === id);
  if (!release) {
    return;
  }

  editingReleaseId = id;
  releaseForm.product.value = release.product;
  releaseForm.version.value = release.version;
  releaseForm.teamName.value = getEditableTeamName(release);
  releaseForm.title.value = release.title;
  releaseForm.description.value = release.description;
  releaseForm.releaseDate.value = release.releaseDate;
  releaseForm.breaking.checked = Boolean(release.isBreaking);
  clearTeamNameError();

  submitButton.textContent = "Update Release Note";
  cancelEditButton.hidden = false;
  releaseForm.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetEditMode() {
  editingReleaseId = null;
  submitButton.textContent = "Add Release Note";
  cancelEditButton.hidden = true;
  releaseForm.reset();
  clearTeamNameError();
}

function deleteRelease(id) {
  const confirmed = window.confirm("Delete this release note?");
  if (!confirmed) {
    return;
  }

  releases = releases.filter((release) => release.id !== id);
  if (editingReleaseId === id) {
    resetEditMode();
  }

  saveReleases(releases);
  renderReleaseList();
}

function generateId() {
  if (window.crypto && typeof window.crypto.randomUUID === "function") {
    return window.crypto.randomUUID();
  }

  return `r-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
}

function exportReleasesCsv() {
  const visibleReleases = getFilteredReleases();
  const rows = [
    ["product", "version", "teamName", "title", "description", "releaseDate", "isBreaking"]
  ];

  for (const release of visibleReleases) {
    rows.push([
      release.product,
      release.version,
      getDisplayTeamName(release),
      release.title,
      release.description,
      release.releaseDate,
      release.isBreaking ? "yes" : "no"
    ]);
  }

  const csv = rows.map((row) => row.map(escapeCsvValue).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const timestamp = getYearMonthStamp();

  link.href = url;
  link.download = `release-notes-${timestamp}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);

  setTransferStatus(`Exported ${visibleReleases.length} visible release notes to CSV.`, "success");
}

function importReleasesFromFile(file) {
  const reader = new FileReader();

  reader.onload = () => {
    try {
      const text = typeof reader.result === "string" ? reader.result : "";
      const parsed = JSON.parse(text);
      const normalized = normalizeImportedReleases(parsed);

      const confirmed = window.confirm(
        `Import ${normalized.length} release notes and replace current data?`
      );
      if (!confirmed) {
        setTransferStatus("Import canceled.", "");
        return;
      }

      releases = normalized;
      resetEditMode();
      saveReleases(releases);
      renderReleaseList();
      setTransferStatus(`Imported ${releases.length} release notes successfully.`, "success");
    } catch (error) {
      setTransferStatus(`Import failed: ${getImportErrorMessage(error)}`, "error");
    }
  };

  reader.onerror = () => {
    setTransferStatus("Import failed: unable to read selected file.", "error");
  };

  reader.readAsText(file);
}

function normalizeImportedReleases(value) {
  if (!Array.isArray(value)) {
    throw new Error("JSON must be an array of release notes.");
  }

  return value.map((item, index) => {
    if (!item || typeof item !== "object") {
      throw new Error(`Item ${index + 1} must be an object.`);
    }

    const product = String(item.product || "").trim();
    const version = String(item.version || "").trim();
    const teamName = String(item.teamName || "").trim();
    const title = String(item.title || "").trim();
    const description = String(item.description || "").trim();
    const releaseDate = String(item.releaseDate || "").trim();

    if (!product || !version || !title || !description || !releaseDate) {
      throw new Error(`Item ${index + 1} is missing required fields.`);
    }

    return {
      id: typeof item.id === "string" && item.id.trim() ? item.id.trim() : generateId(),
      product,
      version,
      teamName: teamName || undefined,
      title,
      description,
      releaseDate,
      isBreaking: Boolean(item.isBreaking)
    };
  });
}

function setTransferStatus(message, kind) {
  transferStatus.textContent = message;
  transferStatus.classList.remove("error", "success");
  if (kind) {
    transferStatus.classList.add(kind);
  }
}

function getImportErrorMessage(error) {
  if (error instanceof Error && error.message) {
    return error.message;
  }

  return "unexpected error";
}

function getFilteredReleases() {
  const selectedProduct = productFilterInput.value;
  const breakingQuery = breakingFilterSelect.value;
  const searchQuery = searchFilterInput.value.trim().toLowerCase();
  const searchKeywords = searchQuery.length > 0 ? searchQuery.split(/\s+/) : [];

  return releases.filter((release) => {
    const matchesProduct = selectedProduct === "all" || release.product === selectedProduct;
    const matchesBreaking =
      breakingQuery === "all" ||
      (breakingQuery === "breaking" && release.isBreaking) ||
      (breakingQuery === "non-breaking" && !release.isBreaking);

    let matchesSearch = searchKeywords.length === 0;
    if (!matchesSearch) {
      const releaseText = `${release.title} ${release.description}`.toLowerCase();
      matchesSearch = searchKeywords.some((keyword) => releaseText.includes(keyword));
    }

    return matchesProduct && matchesBreaking && matchesSearch;
  });
}

function updateProductFilterOptions() {
  const currentSelection = productFilterInput.value || "all";
  const products = Array.from(new Set(releases.map((release) => release.product))).sort((a, b) =>
    a.localeCompare(b)
  );

  productFilterInput.innerHTML = "";
  const allOption = document.createElement("option");
  allOption.value = "all";
  allOption.textContent = "All products";
  productFilterInput.appendChild(allOption);

  for (const product of products) {
    const option = document.createElement("option");
    option.value = product;
    option.textContent = product;
    productFilterInput.appendChild(option);
  }

  if (currentSelection !== "all" && products.includes(currentSelection)) {
    productFilterInput.value = currentSelection;
  } else {
    productFilterInput.value = "all";
  }
}

function getYearMonthStamp() {
  const now = new Date();
  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0");
  return `${year}-${month}`;
}

function escapeCsvValue(value) {
  const text = String(value ?? "");
  return `"${text.replace(/"/g, '""')}"`;
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric"
  });
}

function getDisplayTeamName(release) {
  return typeof release.teamName === "string" && release.teamName.trim()
    ? release.teamName.trim()
    : "Unknown";
}

function getEditableTeamName(release) {
  return typeof release.teamName === "string" ? release.teamName.trim() : "";
}

function showTeamNameError(message) {
  teamNameError.textContent = message;
  teamNameInput.classList.add("input-error");
}

function clearTeamNameError() {
  teamNameError.textContent = "";
  teamNameInput.classList.remove("input-error");
}

function seedData() {
  const initial = [
    {
      id: "r1",
      product: "Billing API",
      version: "v1.4.0",
      teamName: "Platform Team",
      title: "Invoice export now supports CSV and XLSX",
      description: "Added dual-format export and improved export speed for large accounts.",
      releaseDate: "2026-06-08",
      isBreaking: false
    },
    {
      id: "r2",
      product: "Auth Service",
      version: "v2.0.0",
      teamName: "Identity Team",
      title: "Token introspection endpoint updated",
      description: "Old response shape is deprecated. Clients should migrate to the new claims object format.",
      releaseDate: "2026-06-10",
      isBreaking: true
    }
  ];

  saveReleases(initial);
  return initial;
}

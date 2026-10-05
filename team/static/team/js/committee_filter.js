document.addEventListener("DOMContentLoaded", function () {
    const divisionSelect = document.getElementById("committee-division");
    const districtSelect = document.getElementById("committee-district");
    const upazilaSelect = document.getElementById("committee-upazila");
    const municipalitySelect = document.getElementById("committee-municipality");
    const unionWardSelect = document.getElementById("committee-union-ward");

    if (!divisionSelect) {
        return;
    }

    const selectedDistrict = divisionSelect.dataset.selectedDistrict || "";
    const selectedUpazila = divisionSelect.dataset.selectedUpazila || "";
    const selectedMunicipality =
        divisionSelect.dataset.selectedMunicipality || "";
    const selectedUnionWard =
        divisionSelect.dataset.selectedUnionWard || "";


    function resetSelect(select, label) {
        select.innerHTML = "";

        const option = document.createElement("option");
        option.value = "";
        option.textContent = label;

        select.appendChild(option);
    }


    function addOptions(select, results, selectedValue = "") {
        results.forEach(function (item) {
            const option = document.createElement("option");

            option.value = item.id;
            option.textContent = item.name;

            if (String(item.id) === String(selectedValue)) {
                option.selected = true;
            }

            select.appendChild(option);
        });
    }


    async function loadDistricts(divisionId, selectedValue = "") {
        resetSelect(districtSelect, "All Districts");
        resetSelect(upazilaSelect, "All Upazilas");
        resetSelect(municipalitySelect, "All Municipalities");
        resetSelect(unionWardSelect, "All Union / Wards");

        if (!divisionId) {
            return;
        }

        const response = await fetch(
            `/team/ajax/districts/?division_id=${divisionId}`
        );

        const data = await response.json();

        addOptions(
            districtSelect,
            data.results,
            selectedValue
        );
    }


    async function loadUpazilas(districtId, selectedValue = "") {
        resetSelect(upazilaSelect, "All Upazilas");
        resetSelect(municipalitySelect, "All Municipalities");
        resetSelect(unionWardSelect, "All Union / Wards");

        if (!districtId) {
            return;
        }

        const response = await fetch(
            `/team/ajax/upazilas/?district_id=${districtId}`
        );

        const data = await response.json();

        addOptions(
            upazilaSelect,
            data.results,
            selectedValue
        );
    }


    async function loadMunicipalities(upazilaId, selectedValue = "") {
        resetSelect(
            municipalitySelect,
            "All Municipalities"
        );

        if (!upazilaId) {
            return;
        }

        const response = await fetch(
            `/team/ajax/municipalities/?upazila_id=${upazilaId}`
        );

        const data = await response.json();

        addOptions(
            municipalitySelect,
            data.results,
            selectedValue
        );
    }


    async function loadUnionWards(upazilaId, selectedValue = "") {
        resetSelect(
            unionWardSelect,
            "All Union / Wards"
        );

        if (!upazilaId) {
            return;
        }

        const response = await fetch(
            `/team/ajax/union-wards/?upazila_id=${upazilaId}`
        );

        const data = await response.json();

        addOptions(
            unionWardSelect,
            data.results,
            selectedValue
        );
    }


    divisionSelect.addEventListener(
        "change",
        function () {
            loadDistricts(this.value);
        }
    );


    districtSelect.addEventListener(
        "change",
        function () {
            loadUpazilas(this.value);
        }
    );


    upazilaSelect.addEventListener(
        "change",
        function () {
            loadMunicipalities(this.value);
            loadUnionWards(this.value);
        }
    );


    // Restore selected filters after page reload
    if (divisionSelect.value) {
        loadDistricts(
            divisionSelect.value,
            selectedDistrict
        ).then(function () {

            if (selectedDistrict) {
                loadUpazilas(
                    selectedDistrict,
                    selectedUpazila
                ).then(function () {

                    if (selectedUpazila) {
                        loadMunicipalities(
                            selectedUpazila,
                            selectedMunicipality
                        );

                        loadUnionWards(
                            selectedUpazila,
                            selectedUnionWard
                        );
                    }

                });
            }

        });
    }
});
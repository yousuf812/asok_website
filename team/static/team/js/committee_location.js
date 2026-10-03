document.addEventListener("DOMContentLoaded", function () {
    const divisionField = document.getElementById("id_division");
    const districtField = document.getElementById("id_district");
    const upazilaField = document.getElementById("id_thana_upazila");
    const municipalityField = document.getElementById("id_municipality");
    const unionWardField = document.getElementById("id_union_ward");

    if (!divisionField) {
        return;
    }

    function resetSelect(select, placeholder) {
        select.innerHTML = "";

        const option = document.createElement("option");
        option.value = "";
        option.textContent = placeholder;

        select.appendChild(option);
    }

    function populateSelect(select, results, placeholder) {
        resetSelect(select, placeholder);

        results.forEach(function (item) {
            const option = document.createElement("option");

            option.value = item.id;
            option.textContent = item.name;

            select.appendChild(option);
        });
    }

    // ==========================================
    // Division → District
    // ==========================================

    divisionField.addEventListener("change", function () {

        const divisionId = this.value;

        resetSelect(
            districtField,
            "--------- Select District ---------"
        );

        resetSelect(
            upazilaField,
            "--------- Select Upazila ---------"
        );

        resetSelect(
            municipalityField,
            "--------- Select Municipality ---------"
        );

        resetSelect(
            unionWardField,
            "--------- Select Union / Ward ---------"
        );

        if (!divisionId) {
            return;
        }

        fetch(
            `/team/ajax/districts/?division_id=${divisionId}`
        )
            .then(response => response.json())
            .then(data => {

                populateSelect(
                    districtField,
                    data.results,
                    "--------- Select District ---------"
                );

            })
            .catch(error => {
                console.error(
                    "District loading error:",
                    error
                );
            });
    });


    // ==========================================
    // District → Upazila
    // ==========================================

    districtField.addEventListener("change", function () {

        const districtId = this.value;

        resetSelect(
            upazilaField,
            "--------- Select Upazila ---------"
        );

        resetSelect(
            municipalityField,
            "--------- Select Municipality ---------"
        );

        resetSelect(
            unionWardField,
            "--------- Select Union / Ward ---------"
        );

        if (!districtId) {
            return;
        }

        fetch(
            `/team/ajax/upazilas/?district_id=${districtId}`
        )
            .then(response => response.json())
            .then(data => {

                populateSelect(
                    upazilaField,
                    data.results,
                    "--------- Select Upazila ---------"
                );

            })
            .catch(error => {
                console.error(
                    "Upazila loading error:",
                    error
                );
            });
    });


    // ==========================================
    // Upazila → Municipality + Union/Ward
    // ==========================================

    upazilaField.addEventListener("change", function () {

        const upazilaId = this.value;

        resetSelect(
            municipalityField,
            "--------- Select Municipality ---------"
        );

        resetSelect(
            unionWardField,
            "--------- Select Union / Ward ---------"
        );

        if (!upazilaId) {
            return;
        }

        // Municipality
        fetch(
            `/team/ajax/municipalities/?upazila_id=${upazilaId}`
        )
            .then(response => response.json())
            .then(data => {

                populateSelect(
                    municipalityField,
                    data.results,
                    "--------- Select Municipality ---------"
                );

            })
            .catch(error => {
                console.error(
                    "Municipality loading error:",
                    error
                );
            });


        // Union / Ward
        fetch(
            `/team/ajax/union-wards/?upazila_id=${upazilaId}`
        )
            .then(response => response.json())
            .then(data => {

                populateSelect(
                    unionWardField,
                    data.results,
                    "--------- Select Union / Ward ---------"
                );

            })
            .catch(error => {
                console.error(
                    "Union/Ward loading error:",
                    error
                );
            });
    });
});
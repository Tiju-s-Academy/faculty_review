odoo.define('faculty_review.rating', function (require) {
    'use strict';

    function updateHiddenInput(starGroup) {
        const checkedStar = starGroup.querySelector('input[type="radio"]:checked');
        const hiddenInput = starGroup.querySelector('input[type="hidden"]');
        if (checkedStar && hiddenInput) {
            hiddenInput.value = checkedStar.value;
            console.log('Rating updated:', hiddenInput.name, hiddenInput.value); // Debug log
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        const starGroups = document.querySelectorAll('.rating-stars');
        starGroups.forEach(function (group) {
            const stars = group.querySelectorAll('input[type="radio"]');
            stars.forEach(function (star) {
                star.addEventListener('change', function () {
                    updateHiddenInput(group);
                });
            });
        });
    });
});

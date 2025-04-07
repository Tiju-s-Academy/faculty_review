function initTeacherSelection() {
    var selectedTeachers = [];
    var currentTeacherIndex = 0;

    function handleCardClick(e) {
        var card = e.currentTarget;
        var teacherId = card.getAttribute('data-teacher-id');
        console.log('Card clicked:', teacherId);

        if (card.classList.contains('selected')) {
            card.classList.remove('selected');
            selectedTeachers = selectedTeachers.filter(id => id !== teacherId);
        } else {
            card.classList.add('selected');
            selectedTeachers.push(teacherId);
        }

        var actionButtons = document.querySelector('.action-buttons');
        console.log('Selected teachers:', selectedTeachers.length);
        if (selectedTeachers.length > 0) {
            actionButtons.style.display = 'block';
        } else {
            actionButtons.style.display = 'none';
        }
    }

    // Add click handlers to cards
    var cards = document.querySelectorAll('.teacher-card');
    cards.forEach(function(card) {
        card.addEventListener('click', handleCardClick);
    });

    function showRatingFormForTeacher(teacherId) {
        var ratingForm = document.querySelector('.rating-form');
        if (ratingForm) {
            // Update form title with teacher name
            var teacherCard = document.querySelector(`.teacher-card[data-teacher-id="${teacherId}"]`);
            var teacherName = teacherCard.querySelector('.teacher-name').textContent;
            ratingForm.querySelector('.teacher-name-display').textContent = teacherName;

            // Update hidden teacher ID
            document.getElementById('teacher_id').value = teacherId;

            // Show form
            ratingForm.style.display = 'block';
            window.scrollTo({
                top: ratingForm.offsetTop - 50,
                behavior: 'smooth'
            });
        }
    }

    // Add click handler for Rate Selected Teachers button
    var startRatingBtn = document.querySelector('.start-rating-btn');
    if (startRatingBtn) {
        startRatingBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Rate Selected Teachers clicked');

            // Hide selection section
            var selectionSection = document.querySelector('.teacher-selection-section');
            if (selectionSection) {
                selectionSection.style.display = 'none';
            }

            // Show first teacher's form
            showRatingFormForTeacher(selectedTeachers[currentTeacherIndex]);
        });
    }

    // Add form submit handler
    document.querySelector('.rating-form form').addEventListener('submit', function(e) {
        e.preventDefault();

        // Update hidden rating inputs before submission
        document.querySelectorAll('.rating-stars').forEach(group => {
            const checkedStar = group.querySelector('input[type="radio"]:checked');
            const hiddenInput = group.querySelector('input[type="hidden"]');
            if (checkedStar && hiddenInput) {
                hiddenInput.value = checkedStar.value;
                console.log('Rating value updated:', hiddenInput.name, hiddenInput.value);
            }
        });

        var formData = new FormData(this);

        fetch('/teacher_rating/submit', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                window.location.href = '/institute_rating/form';
            }
        });
    });

    // Add click handler for Rate Institute button
    var rateInstituteBtn = document.querySelector('.rate-institute-btn');
    if (rateInstituteBtn) {
        rateInstituteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Rate Institute clicked');
            var instituteForm = document.querySelector('.institute-rating-form');
            if (instituteForm) {
                instituteForm.style.display = 'block';
                instituteForm.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        });
    }
}

// Ensure the script runs after DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTeacherSelection);
} else {
    initTeacherSelection();
}

let currentTeacherIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up star handlers');

    document.querySelectorAll('.rating-stars input[type="radio"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            const hiddenInput = this.closest('.rating-stars').querySelector('input[type="hidden"]');
            hiddenInput.value = this.value;
            console.log('Star rating changed:', this.name, 'value:', this.value);
        });
    });

    // Mark previously rated teachers
    document.querySelectorAll('.teacher-card').forEach(card => {
        const teacherId = card.dataset.teacherId;
        if (localStorage.getItem(`rated_teacher_${teacherId}`)) {
            card.classList.add('rated');
        }
    });

    // Mark institute if rated
    const instituteCard = document.querySelector('.institute-card');
    if (instituteCard && localStorage.getItem('institute_rated')) {
        instituteCard.classList.add('rated');
    }

    // Handle star ratings
    document.querySelectorAll('.rating-stars').forEach(group => {
        group.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', function() {
                updateHiddenInput(group);
            });
        });
    });
});

function startRating() {
    if (selectedTeachers.size === 0) {
        alert('Please select at least one teacher to rate');
        return;
    }
    document.querySelector('.rating-form').classList.remove('d-none');
    document.querySelector('#rating_form').scrollIntoView({ behavior: 'smooth' });
}

function startRatingProcess() {
    if (selectedTeachers.size === 0) {
        alert('Please select at least one teacher to rate');
        return;
    }
    document.getElementById('teacher-selection').classList.add('d-none');
    showTeacherRatingForm(currentTeacherIndex);
}

function showTeacherRatingForm(index) {
    if (index >= selectedTeachers.size) {
        showInstituteRatingForm();
        return;
    }
    const teacherId = Array.from(selectedTeachers)[index];
    document.getElementById('current-teacher-name').textContent =
        document.querySelector(`.teacher-card[data-teacher-id="${teacherId}"]`).querySelector('.teacher-name').textContent;
    document.getElementById('teacher-rating-form').classList.remove('d-none');
    document.getElementById('current-teacher-id').value = teacherId;
}

function submitTeacherRating() {
    // Store current teacher rating in session
    const formData = new FormData(document.getElementById('teacher-rating-form'));
    const ratings = {};
    formData.forEach((value, key) => { ratings[key] = value; });

    if (!window.teacherRatings) window.teacherRatings = [];
    window.teacherRatings.push(ratings);

    currentTeacherIndex++;
    showTeacherRatingForm(currentTeacherIndex);
}

function showInstituteRatingForm() {
    document.getElementById('teacher-rating-form').classList.add('d-none');
    document.getElementById('institute-rating-form').classList.remove('d-none');
}

function submitFinalRating() {
    const instituteFormData = new FormData(document.getElementById('institute-rating-form'));
    const instituteRatings = {};
    instituteFormData.forEach((value, key) => { instituteRatings[key] = value; });

    // Submit all ratings
    return fetch('/teacher_rating/submit_all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            teacher_ratings: window.teacherRatings,
            institute_rating: instituteRatings
        })
    }).then(() => {
        window.location.href = '/teacher_rating/thank_you';
    });
}

function updateHiddenInput(starGroup) {
    const checkedStar = starGroup.querySelector('input[type="radio"]:checked');
    const hiddenInput = starGroup.querySelector('input[type="hidden"]');
    if (checkedStar && hiddenInput) {
        hiddenInput.value = checkedStar.value;
    }
}

function validateFinalSubmit() {
    let hasTeacherRating = false;
    let hasInstituteRating = false;

    // Check if any teacher is rated
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('rated_teacher_')) {
            hasTeacherRating = true;
            break;
        }
    }

    hasInstituteRating = localStorage.getItem('institute_rated') === 'true';

    if (!hasTeacherRating || !hasInstituteRating) {
        alert('Please rate at least one teacher and the institute before final submission.');
        return false;
    }
    return true;
}

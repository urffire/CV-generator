// Replace this with your actual JSON data or fetch it dynamically
let jsonData;

function createProfile(jsonData) {
    const profileContainer = document.getElementById('profile-container');
    profileContainer.innerHTML = ''; // Clear existing content

    // Profile name
    const nameField = createEditableInput('Full name', 'full-name', jsonData.full_name || '');

    profileContainer.appendChild(nameField);


    // Contact info
    const contactInfoContainer = document.createElement('div');
    contactInfoContainer.classList.add('contact-info');

    // City
    const cityField = createEditableInput('City', 'city', jsonData.city || '');
    contactInfoContainer.appendChild(cityField);
    // Country
    const countryField = createEditableInput('Country', 'country', jsonData.country || '');
    contactInfoContainer.appendChild(countryField);
    // Phone Number
    const phoneNumberField = createEditableInput('Phone Number', 'phone-number', jsonData.phone_number || '');
    contactInfoContainer.appendChild(phoneNumberField);

        const emailNumberField = createEditableInput('Email', 'email', jsonData.email || '');
    contactInfoContainer.appendChild(emailNumberField);



    const summaryField = createEditableTextarea('Summary', 'summary', jsonData.summary || '');
    contactInfoContainer.appendChild(summaryField);

    const otherField = createEditableTextarea('Other', 'other', jsonData.other || '');
    contactInfoContainer.appendChild(otherField);

    profileContainer.appendChild(contactInfoContainer);


    // Education list
    const educationList = document.createElement('ul');
    educationList.id = 'education-list';
        const educationHeader = document.createElement('h6');
    educationHeader.textContent = 'Education:';
    educationHeader.classList.add('h3class');
    educationHeader.classList.add('section-header');
    profileContainer.appendChild(educationHeader);

    profileContainer.appendChild(educationList);

    jsonData.education.forEach((education, index) => {
        createEducationEntry(education, index);
    });

    // Add Education button
    const addEducationButton = document.createElement('button');
    addEducationButton.textContent = '+ Add Education';
    addEducationButton.classList.add("btn");
    addEducationButton.classList.add("btn-primary");
    addEducationButton.classList.add("mb-2");
    addEducationButton.onclick = () => createEducationEntry({}, document.querySelectorAll('#education-list li').length);
    profileContainer.appendChild(addEducationButton);
    profileContainer.appendChild(document.createElement('br'));


    // Work Experience list
    const experiencesList = document.createElement('ul');
    experiencesList.id = 'experiences-list';
    const experienceHeader = document.createElement('h6');
    experienceHeader.textContent = 'Work Experience:';
    experienceHeader.classList.add('h3class');
    experienceHeader.classList.add('section-header');
    profileContainer.appendChild(experienceHeader);

    profileContainer.appendChild(experiencesList);

    jsonData.experiences.forEach((experience, index) => {
        createExperienceEntry(experience, index);
    });

    // Add Work Experience button
    const addExperienceButton = document.createElement('button');
    addExperienceButton.textContent = '+ Add Work Experience';
    addExperienceButton.classList.add("btn");
    addExperienceButton.classList.add("btn-primary");
    addExperienceButton.classList.add("mb-2");
    addExperienceButton.onclick = () => createExperienceEntry({}, document.querySelectorAll('#experiences-list li').length);
    profileContainer.appendChild(addExperienceButton);
    profileContainer.appendChild(document.createElement('br'));

    // ... (unchanged)
}

function createEducationEntry(education, index) {


    const educationItem = document.createElement('li');
    const educationContent = document.createElement('div');
    educationContent.classList.add('work-experience-entry');
    const schoolNameField = createEditableInput('School Name', `education-school-name-${index}`, education?.school || '');
    const startField = createEditableInput('Start', `education-starts-at-${index}`, education?.starts_at || '');
    const endField = createEditableInput('End', `education-ends-at-${index}`, education?.ends_at || '');
    const degreeField = createEditableInput('Degree', `education-degree-${index}`, education?.degree_name || '');
    const fieldOfStudyField = createEditableInput('Field of Study', `education-field-of-study-${index}`, education?.field_of_study || '');
    const descriptionField = createEditableTextarea('Description', `education-description-${index}`, education?.description || '');

    educationContent.appendChild(schoolNameField);

    educationContent.appendChild(startField);
    educationContent.appendChild(endField);
    educationContent.appendChild(degreeField);

    educationContent.appendChild(fieldOfStudyField);

    educationContent.appendChild(descriptionField);

    // Remove Education button
    const removeEducationButton = document.createElement('button');
    removeEducationButton.textContent = '- Remove Education';
    removeEducationButton.classList.add("btn");
    removeEducationButton.classList.add("btn-danger");
    removeEducationButton.classList.add("mb-2");
    removeEducationButton.onclick = () => removeEntry('education-list', educationItem, false);
    educationContent.appendChild(removeEducationButton);

    educationItem.appendChild(educationContent);
    document.getElementById('education-list').appendChild(educationItem);
    updateEducationIds();
}

function createExperienceEntry(experience, index) {
    const experienceContent = document.createElement('li');
    const experienceDiv = document.createElement('div');
    experienceContent.classList.add('work-experience-entry');
    const titleField = createEditableInput('Title', `experience-title-${index}`, experience?.title || '');
    const companyLinkField = createEditableInput('Company Link', `experience-company-link-${index}`, experience?.company_linkedin_profile_url || '');
    const startField = createEditableInput('Start', `experience-starts-at-${index}`, experience?.starts_at || '');
    const endField = createEditableInput('End', `experience-ends-at-${index}`, experience?.ends_at || 'Present');
    const descriptionField = createEditableTextarea('Description', `experience-description-${index}`, experience?.description || '');


    experienceDiv.appendChild(titleField);

    experienceDiv.appendChild(companyLinkField);

    experienceDiv.appendChild(startField);
    experienceDiv.appendChild(endField);

    experienceDiv.appendChild(descriptionField);

    // Remove Experience button
    const removeExperienceButton = document.createElement('button');
    removeExperienceButton.textContent = '- Remove Work Experience';
    removeExperienceButton.classList.add("btn");
    removeExperienceButton.classList.add("btn-danger");
    removeExperienceButton.classList.add("mb-2");
    removeExperienceButton.onclick = () => removeEntry('experiences-list', experienceContent, true);
    experienceDiv.appendChild(removeExperienceButton);

    experienceContent.appendChild(experienceDiv);
    document.getElementById('experiences-list').appendChild(experienceContent);
    updateExperienceIds();
}

// New function to update education IDs
function updateEducationIds() {
    const educationItems = document.querySelectorAll('#education-list li');
    educationItems.forEach((educationItem, index) => {
        const fields = educationItem.querySelectorAll('.editable-input-container input, .editable-input-container textarea');
        fields.forEach(field => {
            const oldId = field.id;
            const newId = oldId.replace(/\d+/g, index);
            field.id = newId;
        });
    });
}

// New function to update experience IDs
function updateExperienceIds() {
    const experienceItems = document.querySelectorAll('#experiences-list li');
    experienceItems.forEach((experienceItem, index) => {
        const fields = experienceItem.querySelectorAll('.editable-input-container input, .editable-input-container textarea');
        fields.forEach(field => {
            const oldId = field.id;
            const newId = oldId.replace(/\d+/g, index);
            field.id = newId;
        });
    });
}

function createEditableInput(label, id, value) {
    const container = document.createElement('div');
    container.classList.add('editable-input-container');
    container.classList.add('form-group');

    const labelElement = document.createElement('label');
    labelElement.textContent = `${label}:  `;
    container.appendChild(labelElement);

    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.value = value;
    inputField.id = id;
    inputField.classList.add("indented")
    inputField.classList.add("form-control")
    container.appendChild(inputField);

    return container;
}

function createEditableTextarea(label, id, value) {
    const container = document.createElement('div');
    container.classList.add('editable-input-container');
    container.classList.add('form-group');

    const labelElement = document.createElement('label');
    labelElement.textContent = `${label}: `;
    container.appendChild(labelElement);

    const inputField = document.createElement('textarea');
    inputField.type = 'text';
    inputField.value = value;
    inputField.id = id;
    inputField.classList.add("indented")
    inputField.classList.add("form-control")
    container.appendChild(inputField);

    return container;
}

function removeEntry(listId, entry, exp=true) {
    const list = document.getElementById(listId);
    list.removeChild(entry);
    if (exp)
        updateExperienceIds();
    else
        updateEducationIds();
}

function getEditedProfileData() {
    const editedData = {
        city: document.getElementById('city').value,
        country: document.getElementById('country').value,
        full_name: document.getElementById('full-name').value,
        phone_number: document.getElementById('phone-number').value,
        email: document.getElementById('email').value,
        other: document.getElementById('other').value,

        summary: document.getElementById('summary').value,

        education: [],
        experiences: []
    };

    // Gather edited education data
    const educationItems = document.querySelectorAll('#education-list li');
    educationItems.forEach((educationItem, index) => {
        const educationData = {
            school: getValueByField(`education-school-name-${index}`),
            starts_at: getValueByField(`education-starts-at-${index}`),
            ends_at: getValueByField(`education-ends-at-${index}`),
            degree_name: getValueByField(`education-degree-${index}`),
            field_of_study: getValueByField(`education-field-of-study-${index}`),
            description: getValueByField(`education-description-${index}`)
        };
        editedData.education.push(educationData);
    });

    // Gather edited experience data
    const experienceItems = document.querySelectorAll('#experiences-list li');
    experienceItems.forEach((experienceItem, index) => {
        const experienceData = {
            title: getValueByField(`experience-title-${index}`),
            company_linkedin_profile_url: getValueByField(`experience-company-link-${index}`),
            starts_at: getValueByField(`experience-starts-at-${index}`),
            ends_at: getValueByField(`experience-ends-at-${index}`),
            description: getValueByField(`experience-description-${index}`)
        };
        editedData.experiences.push(experienceData);
    });

    return editedData;
}

// Helper function to get the value of an input field by ID
function getValueByField(fieldId) {
    return document.getElementById(fieldId).value;
}

function saveProfile(doAlert = true) {
    jsonData = getEditedProfileData()

    fetch('/save_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    }).then(response=> response.json()).then(data => {
        if (doAlert) {
            alert(data.message);  // Display the server's response message
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Failed to save profile data.');
    });
}

function loadProfile() {
    // Request the profile data from the server
    fetch('/load_profile').then(response =>
        response.json()
    ).then(profile => {
        createProfile(profile);

        jsonData = profile
    }).catch(error => {
        console.error('Error:', error);
        alert('Failed to load profile data.');
    });
}

loadProfile();

async function fetchProfile() {
    const linkedinUrl = document.getElementById('linkedin').value;

    try {
        const response = await fetch('/fetch_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({linkedin_url: linkedinUrl}),
        });

        if (response.ok) {
            const profileData = await response.json();

            createProfile(profileData)
        } else {
            console.error(`Error: ${response.status} - ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
    }
}

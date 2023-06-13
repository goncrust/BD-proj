const addBtn = document.getElementById("add");
const delBtn = document.getElementById("delete");
const form = document.querySelector("form");

const onChangeDel = (e) => {
  if (delBtn.checked) {
    const prevFieldset = document.querySelector("fieldset");
    if (prevFieldset) prevFieldset.remove();

    const fieldset = document.createElement("fieldset");
    const label = document.createElement("label");
    const input = document.createElement("input");
    const submit = document.createElement("input");
    const br = Array.apply(0, Array(2)).map(() => document.createElement("br"));

    submit.type = "submit";
    submit.value = "Submit";

    label.for = "id";
    label.id = "id-label";
    label.innerHTML = "ID do Cliente";
    input.type = "text";
    input.id = "id";
    input.setAttribute("required", "");

    fieldset.appendChild(label);
    fieldset.appendChild(br[0]);
    fieldset.appendChild(input);
    fieldset.appendChild(br[1]);

    fieldset.appendChild(submit);

    form.appendChild(fieldset);
  }
};

const onChangeAdd = (e) => {
  if (addBtn.checked) {
    const prevFieldset = document.querySelector("fieldset");
    if (prevFieldset) prevFieldset.remove();

    const fieldset = document.createElement("fieldset");
    const nameLabel = document.createElement("label");
    const nameInput = document.createElement("input");
    const emailLabel = document.createElement("label");
    const emailInput = document.createElement("input");
    const phoneLabel = document.createElement("label");
    const phoneInput = document.createElement("input");
    const addressLabel = document.createElement("label");
    const addressInput = document.createElement("input");
    const submit = document.createElement("input");
    const br = Array.apply(0, Array(8)).map(() => document.createElement("br"));

    submit.type = "submit";
    submit.value = "Submit";

    nameLabel.for = "name";
    nameLabel.id = "name-label";
    nameLabel.innerHTML = "Name";
    nameInput.type = "text";
    nameInput.id = "name";
    nameInput.setAttribute("required", "");

    emailLabel.for = "email";
    emailLabel.id = "email-label";
    emailLabel.innerHTML = "Email";
    emailInput.type = "email";
    emailInput.id = "email";
    emailInput.setAttribute("required", "");

    phoneLabel.for = "phone";
    phoneLabel.id = "phone-label";
    phoneLabel.innerHTML = "Phone";
    phoneInput.type = "number";
    phoneInput.id = "phone";
    phoneInput.setAttribute("required", "");

    addressLabel.for = "address";
    addressLabel.id = "address-label";
    addressLabel.innerHTML = "Address";
    addressInput.type = "text";
    addressInput.id = "address";
    addressInput.setAttribute("required", "");

    fieldset.appendChild(nameLabel);
    fieldset.appendChild(br[0]);
    fieldset.appendChild(nameInput);
    fieldset.appendChild(br[1]);

    fieldset.appendChild(emailLabel);
    fieldset.appendChild(br[2]);
    fieldset.appendChild(emailInput);
    fieldset.appendChild(br[3]);

    fieldset.appendChild(phoneLabel);
    fieldset.appendChild(br[4]);
    fieldset.appendChild(phoneInput);
    fieldset.appendChild(br[5]);

    fieldset.appendChild(addressLabel);
    fieldset.appendChild(br[6]);
    fieldset.appendChild(addressInput);
    fieldset.appendChild(br[7]);

    fieldset.appendChild(submit);

    form.appendChild(fieldset);
  }
};

delBtn.addEventListener("change", onChangeDel);
addBtn.addEventListener("change", onChangeAdd);


const flatpicker = flatpickr("#datetimeDisplay", {
    enableTime: true,
    dateFormat: "Y-m-dTH:i",
    inline: true,
});

function setDateTime(dateTime) {
    flatpicker.setDate(dateTime)
}
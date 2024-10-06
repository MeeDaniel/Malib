const volume_modal                = document         .getElementById('volume');
const volume_modal_form           = volume_modal     .querySelector ('form[name="form"]');
const volume_modal_title          = volume_modal_form.querySelector ('input[name="title"]');
const volume_modal_description    = volume_modal_form.querySelector ('textarea');
const volume_modal_cover_image    = volume_modal_form.querySelector ('img');
const volume_modal_cover_fallback = volume_modal_form.querySelector ('.fallback');
const volume_modal_cover_art_link = volume_modal_form.querySelector ('input[name="cover_art_link"]');
const volume_modal_state          = volume_modal_form.querySelector ('select');
const volume_modal_cancel         = volume_modal_form.querySelector ('input[name="cancel"]');
const volume_modal_delete_button  = volume_modal_form.querySelector ('input[name="delete"]');

const volume_modal_delete_form        = volume_modal            .querySelector('form[name="delete"]');
const volume_modal_delete_form_title  = volume_modal_delete_form.querySelector('p > span');

const delete_state_form = document         .getElementById('deleteState');
const delete_state_name = delete_state_form.querySelector('strong');

const add_volume        = document  .getElementById('addVolume');
const add_volume_select = add_volume.querySelector('select');

const states = document.getElementById('states');

function set_volume(volume) {
    volume_modal_cover_fallback.style.display = 'none';
    volume_modal_cover_image   .style.display = '';

    volume_modal_title         .value = volume.title;
    volume_modal_description   .value = volume.description;
    volume_modal_cover_art_link.value = volume.cover_art_link;
    volume_modal_cover_image   .src   = volume.cover_art_link;
    volume_modal_state         .value = volume.state;

    volume_modal_delete_form_title.innerHTML = volume.title;
}

function open_volume(volume) {
    volume_modal.style.display = 'flex';
    volume_modal_form.action = '/edit_volume/' + volume._id;
    set_volume(volume);
    volume_modal_delete_button.onclick = () => {
        open_volume_delete_notice(volume);
    }
    close_volume_delete_notice();
    volume_modal_cancel.onclick = () => {
        set_volume(volume);
    }
    volume_modal_delete_form.action = '/delete_volume/' + volume._id;
}

function close_volume() {
    volume_modal.style.display = '';
}

function open_volume_delete_notice(volume) {
    volume_modal_delete_form.style.display = 'flex';
}

function close_volume_delete_notice() {
    volume_modal_delete_form.style.display = '';
}

function set_delete_state(state) {
    delete_state_name.innerHTML = state.name;
}

function open_delete_state(state) {
    delete_state_form.style.display = 'block';
    delete_state_form.action = '/delete_state/' + state._id;
    set_delete_state(state)
}

function close_delete_state() {
    delete_state_form.style.display = '';
}

function open_add_volume(state) {
    add_volume.style.display = 'flex';
    add_volume_select.value = state._id;
    add_volume.querySelectorAll('input[name="title"], input[name="description"], input[name="cover_art_link"]').forEach(e => {
        e.value = '';
        console.log(e);
    });
}

function close_add_volume() {
    add_volume.style.display = '';
}

function open_states() {
    states.style.display = 'flex';
}

function close_states() {
    states.style.display = 'none';
}

var getLastPartOfUrl = function ($url) {
    var url = $url;
    var urlsplit = url.split("/");
    var lastpart = urlsplit[urlsplit.length - 1];
    if (lastpart === '') {
        lastpart = urlsplit[urlsplit.length - 2];
    }
    return lastpart;
}

var onRequestSuccess = function (idx, groupId, response) {
    pic_name = response.name;
    // console.log(name)
    objectives = response.objectives;
    var wrapper = $('#' + groupId);
    wrapper.html('');

    var filled_no = false, filled_name = false, filled_link = false, filled_action = false, old_o = null;

    $.each(objectives, function (o_idx, o) {
        // console.log(o.name);
        krs = o.krs;
        $.each(krs, function (kr_idx, kr) {
            // console.log(kr.name, kr.desc);

            var no_tag = $('<td/>');
            // no_tag.attr('rowspan', maxKrs)
            if (!filled_no)
                no_tag.text(idx);
            filled_no = true

            var link_tag = $('<td/></td>');
            // link_tag.attr('rowspan', maxKrs)
            if (!filled_link)
                link_tag.append('<a href="https://goal.sun-asterisk.vn/groups/' + groupId + '" target="_blank">' + groupId + '</a>');
            filled_link = true

            var name_tag = $('<td/>');
            // name_tag.attr('rowspan', maxKrs);
            if (!filled_name)
                name_tag.text(pic_name);
            filled_name = true

            var o_tag = $('<td/>');
            if (old_o !== o.name)
                o_tag.text(o.name + " (" + o.progress + ")");
            old_o = o.name

            var kr_tag = $('<td/>');
            kr_tag.text(kr.name + " (" + kr.progress + ")");

            var kr_target = $('<td/>');
            kr_target.text(kr.target);

            var kr_desc_tag = $('<td class="text-desc"/>');
            kr_desc_tag.text(kr.desc);

            var action_tag = $('<td/>');
            if (!filled_action)
                action_tag.append(getReloadAction(idx, groupId));
            filled_action = true

            var tr = $('<tr/>');
            tr.append(no_tag, link_tag, name_tag, o_tag, kr_tag, kr_target, kr_desc_tag, action_tag);

            wrapper.append(tr);

        })
    })
};

var getReloadAction = function (idx, groupId) {
    var reload = $('<a href="#reload-' + groupId + '" id="reload" class="btn btn-primary btn-sm noExl">Reload</a>');
    reload.click(function (e) {
        e.preventDefault();
        var self = $(this)

        $.ajax({
            url: '/api/group/' + groupId,
            success: function (data) {
                onRequestSuccess(idx, groupId, data)
            },
            error: function () {
                self.text('Reload');
                self.removeClass('disabled');
            },
            beforeSend: function () {
                self.text('Loading');
                self.addClass('disabled');
            },
            complete: function () {
                self.text('Reload');
                self.removeClass('disabled');
            },
            type: 'GET',
            dataType: 'json'
        });
    })
    return reload
}

jQuery(document).ready(function () {
    $('#execute').click(function () {
        var links = $('#links').val().split('\n');
        var output = $('#output-body');
        output.find('tbody').remove();

        for (var i = 0; i < links.length; i++) {
            var groupId = getLastPartOfUrl(links[i])
            var tr = $('<tr/>');

            var no = $('<td>' + (i + 1) + '</td>')
            var link = $('<td><a href="' + links[i] + '" target="_blank">' + groupId + '</a></td>');
            var name = $('<td/>');
            var o = $('<td/>');
            var kr = $('<td/>');
            var target = $('<td/>');
            var desc = $('<td class="text-desc"/>');
            var action = $('<td/>');
            action.html(getReloadAction(i + 1, groupId));
            tr.append(no, link, name, o, kr, target, desc, action);

            var wrapper = $('<tbody/>')
            wrapper.attr('id', groupId);
            wrapper.append(tr)
            output.append(wrapper);

            // TRIGGER ACTION
            action.find('a').trigger('click');
        }
    });

    $('#export').click(function () {
        $("#output-body").table2excel({
            exclude: ".noExl",
            name: "Sheet1",
            filename: "okr-2020.xls",
        });
    })
});

$(document)
    .ajaxStart(function () {
        $('#execute').addClass('disabled');
    })
    .ajaxStop(function () {
        $('#execute').removeClass('disabled');
    });
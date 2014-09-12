<p style="margin: 0 0 10px 0;">
    Greetings {{user.name}}!
</p>

<p style="margin: 0 0 10px 0;">
    This is your summary of completed tasks from {{start.strftime("%B %d, %Y")}} to {{end.strftime("%B %d, %Y")}}.
</p>

% person = None
% date = None
% for task in tasks:
    % if task.user != person:
        % date = None
        <div style="margin: 0 0 10px 0;">
            <h3 style="font-size: 1.2em;">{{task.user.name}}</h3>
    % end

    % if task.date.strftime("%B %D, %Y") != date:
        <div style="margin:0 0 5px 0;">
            <strong>{{(task.date + timezone_correct).strftime("%B %d, %Y")}}</strong>
        </div>
        <ul>
    % end

            <li>{{task.description}}</li>

    % if task.date != date:
        </ul>
    % end

    % if task.user != person:
        </div>
    % end

    % date = task.date.strftime("%B %D, %Y")
    % person = task.user
% end

<p style="margin: 0 0 10px 0; color: #999;">
    This email was created on {{end.strftime("%B %d, %Y at %I:%M:%S %p")}}.
</p>

<p style="margin: 0 0 10px 0; color: #999;">
    For additional information, send an email with 'help' in the subject
    line to {{sender}}.
</p>

<p>
    In service,
    <br>
    TeachBoost Ansible
</p>

<p style="margin: 0 0 10px 0;">
    Greetings {{user.name}}!
</p>

<p style="margin: 0 0 10px 0;">
    This is your summary of completed tasks from {{start.strftime("%B %d, %Y")}} to {{end.strftime("%B %d, %Y")}}.
</p>

% for user_tasks in tasks:
    <div style="margin: 0 0 10px 0;">
        <h3 style="font-size: 1.2em;">{{user_tasks['user']}}</h3>
        % for date_tasks in user_tasks['tasks']:
            <div style="margin:0 0 5px 0;">
                <strong>{{date_tasks['date']}}</strong>
            </div>
            <ul>
                % for task in date_tasks['tasks']:
                    <li>{{task}}</li>
                % end
            </ul>
        %end
    </div>
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

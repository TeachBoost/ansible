<p style="margin: 0 0 10px 0;">
    Greetings {{user.name}}!
<p>

<p style="margin: 0 0 10px 0;">
    The following is a list of all of your digest subscription times:
</p>
<ul style="margin: 0 0 20px 0;">
    % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        <li>
            % subscription = getattr(user, day)
            % suffix = '' if subscription is None else 'PM' if subscription > 12 else 'AM'
            % value = subscription - 12 if subscription > 12 else subscription
            {{day}}: {{value}} {{suffix}}
        </li>
    % end
</ul>

<p style="margin: 0 0 10px 0; color: #999;">
    For additional information, send an email with 'help' in the subject
    line to {{sender}}.
</p>

<p>
    In service,
    <br>
    TeachBoost Ansible
</p>

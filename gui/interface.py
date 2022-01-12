from javax.swing import JPanel, JButton, JTextField, JFrame, BorderFactory, JLabel, GroupLayout, JToggleButton, JCheckBox, SwingConstants, JSeparator
from java.awt import BorderLayout, GridLayout, FlowLayout
from java.awt import Dimension, Font, Color

import logging


class Interface:

    def __init__(self, burp_extender):
        self._extender = burp_extender
        self._main_panel = JPanel()
        self._panel = JPanel()
        self._show_nonce = True
        self._nonce_curr_lbl = JTextField("")
        self._nonce_curr_lbl.setEditable(False)

    def update_nonce(self):
        if not self._show_nonce:
            return
        nonce = self._extender.get_saved_nonce()
        if nonce:
            self._nonce_curr_lbl.setText(nonce)
        else:
            self._nonce_curr_lbl.setText("N.A.")

    def clear_nonce(self):
        self._nonce_curr_lbl.setText("")

    def get_main_panel(self):
        return self._main_panel

    def draw_tab(self):

        def btn1Click(event):
            self._extender.set_username(usr_txt.getText())
            self._extender.set_password(pwd_txt.getText())
            return

        def btn2Click(event):
            if(self._extender.get_enabled()):
                self._extender.set_enabled(False)
                btn2.setSelected(False)
                btn2.text = "Digest Auth is off"
            else:
                self._extender.set_enabled(True)
                btn2.setSelected(True)
                btn2.text = "Digest Auth is on"
            return

        def auto_update_check(event):
            if(nonce_chk.isSelected()):
                logging.debug("auto-update checked")
                self._extender.set_auto_update_nonce(True)
            else:
                logging.debug("auto-update un-checked")
                self._extender.set_auto_update_nonce(False)

        def use_suite_scope_check(event):
            if(scope_chk.isSelected()):
                logging.debug("use suite scope checked")
                self._extender.set_use_suite_scope(True)
            else:
                logging.debug("use suite scope un-checked")
                self._extender.set_use_suite_scope(False)

        def tools_check(event):
            cmd = event.getActionCommand()
            logging.debug("Toggling: {}".format(cmd))
            if cmd in self._extender.get_tools():
                self._extender.del_tool(cmd)
            else:
                self._extender.add_tool(cmd)

        def toggle_show_nonce(event):
            if self._show_nonce:
                self._show_nonce = False
                self.clear_nonce()
            else:
                self._show_nonce = True
                self.update_nonce()
            

        ban_lbl = JLabel("HTTP Digest Authentication")
        ban_fnt = ban_lbl.getFont().getName()
        ban_lbl.setFont(Font(ban_fnt, Font.BOLD, 18))
        ban2_lbl = JLabel("by pyno")
        sep_lbl = JSeparator(SwingConstants.HORIZONTAL)
        sep_pad = JLabel("  ")
    
        btn1 = JButton("Save", actionPerformed=btn1Click)

        btn2 = None
        if self._extender.get_enabled():
            btn2 = JToggleButton("Digest Auth is on", actionPerformed=btn2Click)
            btn2.setSelected(True)
        else:
            btn2 = JToggleButton("Digest Auth is off", actionPerformed=btn2Click)
            btn2.setSelected(False)

        usr_lbl = JLabel("Username")
        usr_txt = JTextField(self._extender.get_username())

        pwd_lbl = JLabel("Password")
        pwd_txt = JTextField(self._extender.get_password())
        pwd_txt.setPreferredSize(Dimension(400,1))

        cred_lbl = JLabel("Credentials")
        cred_fnt = cred_lbl.getFont().getName()
        cred_lbl.setFont(Font(cred_fnt, Font.BOLD, 14))

        nonce_lbl = JLabel("Nonce")
        nonce_fnt = nonce_lbl.getFont().getName()
        nonce_lbl.setFont(Font(nonce_fnt, Font.BOLD, 14))

        nonce_chk = JCheckBox("Auto-update nonce", self._extender.get_auto_update_nonce(), 
                actionPerformed=auto_update_check)

        nonce_curr_chk  = JCheckBox("Show current nonce", self._show_nonce, actionPerformed=toggle_show_nonce)
    
        tools_lbl = JLabel("Tools")
        tools_fnt = tools_lbl.getFont().getName()
        tools_lbl.setFont(Font(tools_fnt, Font.BOLD, 14))
        repeater_chk = JCheckBox("Repeater", "Repeater" in self._extender.get_tools(), 
                actionPerformed=tools_check)
        scanner_chk = JCheckBox("Scanner", "Scanner" in self._extender.get_tools(), 
                actionPerformed=tools_check)
        intruder_chk = JCheckBox("Intruder", "Intruder" in self._extender.get_tools(), 
                actionPerformed=tools_check)
        proxy_chk = JCheckBox("Proxy", "Proxy" in self._extender.get_tools(), 
                actionPerformed=tools_check)

        scope_lbl = JLabel("Scope")
        scope_fnt = scope_lbl.getFont().getName()
        scope_lbl.setFont(Font(scope_fnt, Font.BOLD, 14))
        scope_chk = JCheckBox("Use suite scope", self._extender.get_use_suite_scope(),
                actionPerformed=use_suite_scope_check)

        layout = GroupLayout(self._panel)
        self._panel.setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)

        hGroup = layout.createParallelGroup(GroupLayout.Alignment.CENTER) 

        hGroup.addComponent(ban_lbl)
        hGroup.addComponent(ban2_lbl)
        hGroup.addComponent(sep_lbl)
        hGroup.addComponent(sep_pad)
        hGroup.addComponent(btn2)
        hGroup.addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(cred_lbl)
                    .addComponent(usr_lbl)
                    .addComponent(pwd_lbl)
                    .addComponent(btn1)
                    .addComponent(nonce_lbl)
                    .addComponent(nonce_chk)
                    .addComponent(nonce_curr_chk)
                    .addComponent(tools_lbl)
                    .addComponent(repeater_chk)
                    .addComponent(scanner_chk)
                    .addComponent(intruder_chk)
                    .addComponent(proxy_chk)
                    .addComponent(scope_lbl)
                    .addComponent(scope_chk))
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(usr_txt)
                    .addComponent(pwd_txt)
                    .addComponent(self._nonce_curr_lbl)))

        layout.setHorizontalGroup(hGroup)
        
        vGroup = layout.createSequentialGroup()
        vGroup.addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup()
                    .addComponent(ban_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(ban2_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_pad))
                .addGroup(layout.createParallelGroup()
                    .addComponent(btn2))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_pad))
                .addGroup(layout.createParallelGroup()
                    .addComponent(cred_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(usr_lbl)
                    .addComponent(usr_txt))
                .addGroup(layout.createParallelGroup()
                    .addComponent(pwd_lbl)
                    .addComponent(pwd_txt))
                .addGroup(layout.createParallelGroup()
                    .addComponent(btn1))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_pad))
                .addGroup(layout.createParallelGroup()
                    .addComponent(nonce_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(nonce_chk))
                .addGroup(layout.createParallelGroup()
                    .addComponent(nonce_curr_chk)
                    .addComponent(self._nonce_curr_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_pad))
                .addGroup(layout.createParallelGroup()
                    .addComponent(tools_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(repeater_chk))
                .addGroup(layout.createParallelGroup()
                    .addComponent(scanner_chk))
                .addGroup(layout.createParallelGroup()
                    .addComponent(intruder_chk))
                .addGroup(layout.createParallelGroup()
                    .addComponent(proxy_chk))
                .addGroup(layout.createParallelGroup()
                    .addComponent(sep_pad))
                .addGroup(layout.createParallelGroup()
                    .addComponent(scope_lbl))
                .addGroup(layout.createParallelGroup()
                    .addComponent(scope_chk)))

        layout.setVerticalGroup(vGroup)

        self._main_panel.add(self._panel)


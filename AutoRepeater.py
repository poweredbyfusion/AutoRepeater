from burp import IBurpExtender, IHttpListener, ITab
from javax.swing import JPanel, JCheckBox, SwingUtilities, BorderFactory
from java.awt import BorderLayout
from java.awt.event import ActionListener

class BurpExtender(IBurpExtender, IHttpListener, ITab, ActionListener):
    def registerExtenderCallbacks(self, callbacks):
        # Set up extension
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Auto Send to Repeater")

        # Register as an HTTP listener
        self.callbacks.registerHttpListener(self)

        # Create GUI components
        self.panel = JPanel(BorderLayout())
        self.toggleCheckBox = JCheckBox("Enable Auto Send to Repeater")
        self.toggleCheckBox.addActionListener(self)
        self.panel.add(self.toggleCheckBox, BorderLayout.NORTH)
        
        # Add tab to Burp's UI
        callbacks.addSuiteTab(self)
        
        # Initialize toggle state
        self.isEnabled = False

    def actionPerformed(self, event):
        # Toggle functionality based on checkbox state
        self.isEnabled = self.toggleCheckBox.isSelected()

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # If enabled, send requests to Repeater
        if self.isEnabled and messageIsRequest:
            http_service = messageInfo.getHttpService()
            self.callbacks.sendToRepeater(
                http_service.getHost(),
                http_service.getPort(),
                http_service.getProtocol().lower() == "https",
                messageInfo.getRequest(),
                None
            )

    def getTabCaption(self):
        # Tab name in Burp Suite
        return "Auto Repeater"
    
    def getUiComponent(self):
        # Return the UI component for the tab
        return self.panel

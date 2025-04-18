# PhantomHop
PhantomHop is a Python-based Tor IP rotation tool designed to enhance anonymity by periodically changing your public IP address using the Tor network. It ensures seamless proxy configuration and automates the process of requesting new Tor circuits.

# Tor-Based IP Spoofing Tool for Anonymity

## Abstract

This Python-based tool leverages the Tor network to dynamically rotate  IP addresses, providing anonymity during online activities. Designed for tasks such as reconnaissance or secure browsing, it routes traffic through Tor's SOCKS5 proxy and rotates IP addresses periodically to minimize traceability. The tool focuses on session-specific proxying, ensuring that all requests made within the same terminal session are anonymized while keeping the rest of the system unaffected. This approach balances automation and privacy, offering users control over their network anonymity. It works on both windows and linux


## Usage Scenarios

- **Reconnaissance:** Anonymous data collection during penetration testing.
- **Secure Browsing:** Shielding browsing activities from being linked to a real IP.
- **Testing Environments:** Verifying the behavior of tools or services under anonymized conditions.

# Setup & Configuration

## 1. Install Tor
- **On Linux**:
    ```bash
    sudo apt update && sudo apt install tor
    ```
- **On Windows**: Download and install Tor from [Tor Project](https://www.torproject.org/download/).

## 2. Tor Service Configuration
- The script assumes Tor is running on control port `9051`.
- **Linux**: The `torrc` file is located at `/etc/tor/torrc`.
- **Windows**: The `torrc` file is located at `C:\Users\YourUsername\AppData\Roaming\tor\torrc`.

## 3. Set Up the Control Port Password
1. Run this command to generate a hashed password:
    ```bash
    tor --hash-password "your-password"
    ```
    Example output: `16:your-hashed-password`
2. Add the following to the `torrc` file:
   - **Linux**: Use `sudo nano /etc/tor/torrc`.
      ```bash
        ControlPort 127.0.0.1:9051
        SocksPort 127.0.0.1:9050
        HashedControlPassword 16:YourHashedPassword
        CookieAuthentication 0
        SocksPolicy accept 127.0.0.1/8
      ```
    
  - **Windows**: Edit `C:\Users\YourUsername\AppData\Roaming\tor\torrc`.
      ``` bash
        ControlPort 127.0.0.1:9051
        SocksPort 127.0.0.1:9050
        HashedControlPassword 16:YourHashedPassword
        CookieAuthentication 0
        SocksPolicy accept 127.0.0.1/8
       
      ```

3. Restart Tor:
    - **Linux**: `sudo systemctl restart tor`
    - **Windows**: Restart from Task Manager or Tor Browser.

## 4. Proxy Configuration
The script automatically configures SOCKS5 proxy to route traffic through Tor. No manual setup required.

## 5. Change Password in the Script
- In the script, the default password is set to `"hello"`, located at line 64:
    ```python
    Connection.authenticate(password="hello")
    ```
- Change `"hello"` to the password you set in the `torrc` file:
    ```python
    Connection.authenticate(password="16:your-hashed-password")
    ```

## Usage Scenarios

- **Reconnaissance:** Anonymous data collection during penetration testing.
- **Secure Browsing:** Shielding browsing activities from being linked to a real IP.
- **Testing Environments:** Verifying the behavior of tools or services under anonymized conditions.





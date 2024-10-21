#!/bin/bash

# Set this variable to "true" to enable debug messages, "false" to disable
enable_log_message=false

# Function to print debug messages only if enable_log_message is true
log_message() {
  if [ "$enable_log_message" = true ]; then
    echo "$1"
  fi
}

# Run xrandr --auto to automatically detect connected displays
log_message "Running xrandr --auto to detect connected displays..."
xrandr --auto

# Get xrandr output and check which displays are connected
log_message "Getting xrandr output..."
xrandr_output=$(xrandr)

# Print xrandr output for debugging
log_message "xrandr output:"
log_message "$xrandr_output"

# Check if eDP-1, DP-1, and HDMI-1-0 are connected
edp1_connected=$(echo "$xrandr_output" | grep -q "eDP-1 connected" && echo "yes" || echo "no")
dp1_connected=$(echo "$xrandr_output" | grep -q "^DP-1 connected" && echo "yes" || echo "no")
hdmi_connected=$(echo "$xrandr_output" | grep -q "^HDMI-1-0 connected" && echo "yes" || echo "no")

# Print connection status for debugging
log_message "Display connection status:"
log_message "eDP-1 connected: $edp1_connected"
log_message "DP-1 connected: $dp1_connected"
log_message "HDMI-1-0 connected: $hdmi_connected"

# Adjust screen layout based on connected displays
if [[ "$edp1_connected" == "yes" && "$dp1_connected" == "yes" ]]; then
  log_message "Configuring eDP-1 and DP-1..."

  # Check if DP-1 has 1920x1080 mode available
  available_modes=$(xrandr | grep -A 5 "DP-1 connected" | grep -oP '\d+x\d+')

  # Print available modes for DP-1
  log_message "Available modes for DP-1: $available_modes"

  if echo "$available_modes" | grep -q "1920x1080"; then
    log_message "Setting DP-1 to 1920x1080 mode..."
    xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal \
      --output DP-1 --mode 1920x1080 --pos 0x0 --rotate normal \
      --output DP-2 --off \
      --output HDMI-1-0 --off
    log_message "eDP-1 and DP-1 configured successfully."
  else
    log_message "1920x1080 mode not available for DP-1. Configuring with default resolution."
    xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal \
      --output DP-1 --auto --pos 0x0 --rotate normal \
      --output DP-2 --off \
      --output HDMI-1-0 --off
  fi
elif [[ "$edp1_connected" == "yes" && "$hdmi_connected" == "yes" ]]; then
  log_message "Configuring eDP-1 and HDMI-1-0..."
  xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal \
    --output DP-1 --off \
    --output DP-2 --off \
    --output HDMI-1-0 --mode 1920x1080 --pos 0x0 --rotate normal
  log_message "eDP-1 and HDMI-1-0 configured successfully."
elif [[ "$edp1_connected" == "yes" ]]; then
  log_message "Configuring only eDP-1..."
  xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal \
    --output DP-1 --off \
    --output DP-2 --off \
    --output HDMI-1-0 --off
  log_message "eDP-1 configured successfully."
else
  log_message "No known monitor configuration detected."
fi

log_message "Display configuration script completed."

/**
 * Loader Component
 */
import React from 'react';
import { View, ActivityIndicator, Text } from 'react-native';

const Loader = ({ visible = false, message = 'Loading...' }) => {
  if (!visible) return null;

  return (
    <View style={{
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    }}>
      <ActivityIndicator size="large" color="#f50057" />
      <Text style={{ color: 'white', marginTop: 10 }}>{message}</Text>
    </View>
  );
};

export default Loader;

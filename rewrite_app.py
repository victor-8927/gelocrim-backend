# Reescreve RotaScreen.js com novo design neon e card completo
rota_screen = r"""import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  ActivityIndicator, Alert, Dimensions, ScrollView, FlatList
} from 'react-native';
import MapView, { Marker, Polyline, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';

const API_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1';
const DEPOSITO = { latitude: -3.093544, longitude: -60.075812 };
const { height, width } = Dimensions.get('window');

// Cores neon por status
const CORES = {
  pending:   '#00BFFF',  // Azul neon
  completed: '#00FF88',  // Verde neon
  failed:    '#FF3355',  // Vermelho neon
  reentrega: '#FFD700',  // Amarelo neon
  adiada:    '#BF5FFF',  // Roxo neon
};

function decodePolyline(encoded) {
  const poly = [];
  let index = 0, lat = 0, lng = 0;
  while (index < encoded.length) {
    let shift = 0, result = 0, b;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lat += (result & 1) ? ~(result >> 1) : (result >> 1);
    shift = 0; result = 0;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lng += (result & 1) ? ~(result >> 1) : (result >> 1);
    poly.push({ latitude: lat / 1e5, longitude: lng / 1e5 });
  }
  return poly;
}

export default function RotaScreen({ navigation, route }) {
  const { token, user } = route.params;
  const mapRef = useRef(null);
  const [stops, setStops]         = useState([]);
  const [rotaInfo, setRotaInfo]   = useState(null);
  const [posicao, setPosicao]     = useState(null);
  const [loading, setLoading]     = useState(true);
  const [semRota, setSemRota]     = useState(false);
  const [rotaCoords, setRotaCoords] = useState([]);
  const [stopSel, setStopSel]     = useState(null);
  const [modoLista, setModoLista] = useState(false);
  const [kmInicial, setKmInicial] = useState(null);
  const [showKm, setShowKm]       = useState(false);
  const [kmInput, setKmInput]     = useState('');

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'ngrok-skip-browser-warning': '1'
  };

  useEffect(() => { iniciarGPS(); carregarRota(); }, []);

  async function iniciarGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({});
      setPosicao({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });
    } catch {}
  }

  async function carregarRota() {
    setLoading(true);
    setSemRota(false);
    try {
      const datas = [];
      for (let i = 0; i < 3; i++) {
        const d = new Date(Date.now() - i * 86400000);
        datas.push(d.toISOString().slice(0, 10));
      }
      let rotaEncontrada = null;
      for (const data of datas) {
        const res = await fetch(`${API_URL}/routes?date=${data}`, { headers });
        if (!res.ok) continue;
        const rotas = await res.json();
        if (!Array.isArray(rotas)) continue;
        const validas = rotas.filter(r => r.status === 'released' || r.status === 'executing');
        if (validas.length > 0) { rotaEncontrada = validas[0]; break; }
      }
      if (!rotaEncontrada) { setSemRota(true); setLoading(false); return; }
      setRotaInfo(rotaEncontrada);

      const resS = await fetch(`${API_URL}/routes/${rotaEncontrada.route_id}/stops`, { headers });
      const stopsData = await resS.json();
      if (Array.isArray(stopsData) && stopsData.length > 0) {
        const sorted = stopsData.sort((a, b) => (a.sequence || 0) - (b.sequence || 0));
        setStops(sorted);
        setTimeout(() => {
          if (mapRef.current) {
            const coords = [DEPOSITO, ...sorted.map(s => ({
              latitude: parseFloat(s.lat), longitude: parseFloat(s.lng)
            }))].filter(c => c.latitude && c.longitude);
            mapRef.current.fitToCoordinates(coords, {
              edgePadding: { top: 100, right: 40, bottom: 280, left: 40 }, animated: true,
            });
          }
        }, 500);
      }
      if (!kmInicial) setShowKm(true);
    } catch (e) {
      Alert.alert('Erro', String(e));
    } finally { setLoading(false); }
  }

  async function iniciarOperacao() {
    if (!kmInicial) { setShowKm(true); return; }
    Alert.alert('Iniciar Operação', 'Confirma início da viagem?', [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Iniciar ▶', onPress: async () => {
        await fetch(`${API_URL}/routes/${rotaInfo.route_id}/iniciar`, { method: 'POST', headers });
        setRotaInfo(p => ({ ...p, status: 'executing' }));
      }}
    ]);
  }

  async function finalizarViagem() {
    Alert.prompt('KM Final', 'Informe o KM final do veículo:', [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Finalizar', onPress: async (kmFinal) => {
        await fetch(`${API_URL}/routes/${rotaInfo.route_id}/finalizar`, {
          method: 'POST', headers,
          body: JSON.stringify({ km_final: kmFinal })
        });
        Alert.alert('✅ Viagem Finalizada!', '', [
          { text: 'OK', onPress: () => navigation.replace('Login') }
        ]);
      }}
    ], 'plain-text', '', 'numeric');
  }

  function getCorStop(stop) {
    if (stop.status === 'completed') return CORES.completed;
    if (stop.status === 'failed')    return CORES.failed;
    if (stop.status === 'reentrega') return CORES.reentrega;
    if (stop.status === 'adiada')    return CORES.adiada;
    const prox = stops.find(s => s.status === 'pending');
    if (prox && prox.stop_id === stop.stop_id) return CORES.pending;
    return 'rgba(255,255,255,0.3)';
  }

  const completadas = stops.filter(s => s.status === 'completed').length;
  const total = stops.length;
  const pct = total > 0 ? Math.round(completadas / total * 100) : 0;
  const proxStop = stops.find(s => s.status === 'pending');

  if (loading) return (
    <View style={styles.center}>
      <Text style={{ fontSize: 48 }}>❄</Text>
      <ActivityIndicator size="large" color="#00BFFF" style={{ marginTop: 16 }} />
      <Text style={styles.loadTxt}>Carregando rota...</Text>
    </View>
  );

  if (semRota) return (
    <View style={styles.center}>
      <Text style={{ fontSize: 48 }}>⏳</Text>
      <Text style={styles.aguardTitulo}>Aguardando Liberação</Text>
      <Text style={styles.aguardSub}>Sua rota ainda não foi autorizada.{'\n'}Aguarde o analista liberar.</Text>
      <TouchableOpacity style={styles.btnVerif} onPress={carregarRota}>
        <Text style={styles.btnVerifTxt}>🔄 Verificar Novamente</Text>
      </TouchableOpacity>
    </View>
  );

  // Modal KM inicial
  if (showKm) return (
    <View style={styles.center}>
      <Text style={{ fontSize: 36, marginBottom: 16 }}>🚛</Text>
      <Text style={styles.aguardTitulo}>KM Inicial</Text>
      <Text style={styles.aguardSub}>Informe o KM atual do veículo para iniciar a operação</Text>
      <View style={styles.kmInput}>
        <Text style={styles.kmInputText}
          onPress={() => {}} suppressHighlighting={true}>
          {kmInput || '0'}
        </Text>
      </View>
      <View style={{ flexDirection: 'row', gap: 8, marginTop: 16 }}>
        {['1','2','3','4','5','6','7','8','9','0','⌫'].map(k => (
          <TouchableOpacity key={k} style={styles.kmKey} onPress={() => {
            if (k === '⌫') setKmInput(p => p.slice(0,-1));
            else setKmInput(p => p + k);
          }}>
            <Text style={styles.kmKeyTxt}>{k}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <TouchableOpacity style={[styles.btnVerif, { marginTop: 24, backgroundColor: '#00BFFF' }]}
        onPress={() => { if(kmInput) { setKmInicial(kmInput); setShowKm(false); } }}>
        <Text style={[styles.btnVerifTxt, { color: '#002855' }]}>✅ Confirmar KM</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <MapView ref={mapRef} style={StyleSheet.absoluteFillObject}
        provider={PROVIDER_GOOGLE}
        initialRegion={{ ...DEPOSITO, latitudeDelta: 0.08, longitudeDelta: 0.08 }}
      >
        {rotaCoords.length > 1 && (
          <Polyline coordinates={rotaCoords} strokeColor="#00BFFF" strokeWidth={4} lineCap="round" />
        )}
        <Marker coordinate={DEPOSITO} anchor={{ x: 0.5, y: 0.5 }}>
          <View style={styles.depositoPin}><Text>🏭</Text></View>
        </Marker>
        {stops.map(stop => {
          const lat = parseFloat(stop.lat), lng = parseFloat(stop.lng);
          if (!lat || !lng) return null;
          const cor = getCorStop(stop);
          return (
            <Marker key={stop.stop_id} coordinate={{ latitude: lat, longitude: lng }}
              onPress={() => { setStopSel(stop); setModoLista(false); }} anchor={{ x: 0.5, y: 0.5 }}>
              <View style={[styles.pin, { backgroundColor: cor, shadowColor: cor }]}>
                <Text style={styles.pinNum}>{(stop.sequence || 0) + 1}</Text>
              </View>
            </Marker>
          );
        })}
        {posicao && (
          <Marker coordinate={posicao} anchor={{ x: 0.5, y: 0.5 }}>
            <View style={styles.motOuter}><View style={styles.motInner} /></View>
          </Marker>
        )}
      </MapView>

      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerBrand}>❄ {rotaInfo?.trip_number || 'GELOCRIM'}</Text>
          <Text style={styles.headerPlaca}>{rotaInfo?.vehicle_plate} · {total} paradas</Text>
        </View>
        <View style={{ alignItems: 'flex-end' }}>
          <Text style={styles.headerPct}>{pct}%</Text>
          <Text style={styles.headerSub}>{completadas}/{total}</Text>
        </View>
      </View>
      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${pct}%` }]} />
      </View>

      {/* Legenda cores */}
      <View style={styles.legenda}>
        {[['🟢','Entregue'],['🟡','Reentrega'],['🔴','Falhou'],['🔵','Próximo']].map(([ic,lb]) => (
          <Text key={lb} style={styles.legendaItem}>{ic} {lb}</Text>
        ))}
      </View>

      {/* Banner iniciar */}
      {rotaInfo?.status === 'released' && (
        <View style={styles.banner}>
          <Text style={styles.bannerTxt}>🟢 Rota liberada! KM: {kmInicial}</Text>
          <TouchableOpacity style={styles.btnIniciar} onPress={iniciarOperacao}>
            <Text style={styles.btnIniciarTxt}>▶ Iniciar</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Botões flutuantes */}
      <View style={styles.botoesFlut}>
        <TouchableOpacity style={styles.btnFlut} onPress={() => { setModoLista(!modoLista); setStopSel(null); }}>
          <Text style={{ fontSize: 18 }}>📋</Text>
        </TouchableOpacity>
        {rotaInfo?.status === 'executing' && (
          <TouchableOpacity style={[styles.btnFlut, { backgroundColor: 'rgba(255,51,85,.3)', borderColor: '#FF3355' }]} onPress={finalizarViagem}>
            <Text style={{ fontSize: 18 }}>🏁</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Card stop selecionado */}
      {stopSel && !modoLista && (
        <View style={[styles.card, { borderColor: getCorStop(stopSel) }]}>
          <View style={{ flexDirection: 'row', alignItems: 'flex-start', gap: 10, marginBottom: 8 }}>
            <View style={[styles.seqBadge, { backgroundColor: getCorStop(stopSel) }]}>
              <Text style={styles.seqTxt}>{(stopSel.sequence || 0) + 1}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.cardLabel}>PRÓXIMA PARADA</Text>
              <Text style={styles.cardNome} numberOfLines={1}>{stopSel.recipient_name}</Text>
              <Text style={styles.cardCod}>COD: {stopSel.codparc || '—'}</Text>
              <Text style={styles.cardEnd} numberOfLines={1}>{stopSel.address}</Text>
            </View>
            <TouchableOpacity onPress={() => setStopSel(null)}>
              <Text style={{ color: '#888', fontSize: 18 }}>✕</Text>
            </TouchableOpacity>
          </View>
          <View style={{ flexDirection: 'row', gap: 12, marginBottom: 12 }}>
            <Text style={styles.metaTxt}>🕐 {stopSel.eta || '--:--'}</Text>
            <Text style={styles.metaTxt}>⚖️ {(stopSel.weight_kg || 0).toFixed(0)}kg</Text>
            <Text style={styles.metaTxt}>📄 {stopSel.num_docs || '—'} docs</Text>
          </View>
          <TouchableOpacity
            style={[styles.btnEntrar, rotaInfo?.status !== 'executing' && { opacity: 0.4 }]}
            disabled={rotaInfo?.status !== 'executing'}
            onPress={() => navigation.navigate('Entrega', {
              stop: stopSel, token, routeId: rotaInfo?.route_id,
              proximoStop: stops.find(s => s.sequence > stopSel.sequence && s.status === 'pending')
            })}
          >
            <Text style={styles.btnEntrarTxt}>
              {rotaInfo?.status === 'executing' ? 'REGISTRAR ENTREGA →' : 'Inicie a operação primeiro'}
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Lista de paradas */}
      {modoLista && (
        <View style={styles.lista}>
          <Text style={styles.listaTitulo}>❄ SEQUÊNCIA DE ENTREGAS</Text>
          <ScrollView showsVerticalScrollIndicator={false}>
            {stops.map(stop => (
              <TouchableOpacity key={stop.stop_id} style={[styles.listaItem, { borderLeftColor: getCorStop(stop), borderLeftWidth: 3 }]}
                onPress={() => {
                  setStopSel(stop); setModoLista(false);
                  mapRef.current?.animateToRegion({
                    latitude: parseFloat(stop.lat), longitude: parseFloat(stop.lng),
                    latitudeDelta: 0.01, longitudeDelta: 0.01
                  }, 600);
                }}>
                <View style={[styles.seqBadge, { backgroundColor: getCorStop(stop), width: 26, height: 26 }]}>
                  <Text style={[styles.seqTxt, { fontSize: 10 }]}>{(stop.sequence || 0) + 1}</Text>
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.listaNome} numberOfLines={1}>{stop.recipient_name}</Text>
                  <Text style={styles.listaCod}>COD: {stop.codparc || '—'} · {stop.address || ''}</Text>
                </View>
                <Text style={styles.listaEta}>{stop.eta || '--:--'}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#001020', padding: 32 },
  loadTxt: { color: 'rgba(255,255,255,0.5)', marginTop: 12, fontSize: 13 },
  aguardTitulo: { color: '#FFFFFF', fontSize: 20, fontWeight: '800', marginTop: 16, textAlign: 'center' },
  aguardSub: { color: 'rgba(255,255,255,0.5)', fontSize: 13, marginTop: 8, textAlign: 'center', lineHeight: 20 },
  btnVerif: { marginTop: 24, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 12, padding: 14, paddingHorizontal: 24, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)' },
  btnVerifTxt: { color: '#FFFFFF', fontWeight: '700', fontSize: 14 },
  kmInput: { backgroundColor: 'rgba(0,191,255,0.1)', borderRadius: 12, padding: 16, width: '80%', borderWidth: 1, borderColor: '#00BFFF', marginTop: 16, alignItems: 'center' },
  kmInputText: { color: '#00BFFF', fontSize: 32, fontWeight: '900' },
  kmKey: { backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 8, width: 44, height: 44, alignItems: 'center', justifyContent: 'center' },
  kmKeyTxt: { color: '#fff', fontSize: 18, fontWeight: '700' },
  header: { position: 'absolute', top: 0, left: 0, right: 0, backgroundColor: 'rgba(0,10,30,0.95)', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 14, paddingTop: 44 },
  headerBrand: { color: '#00BFFF', fontSize: 11, fontWeight: '800', letterSpacing: 4, marginBottom: 2 },
  headerPlaca: { color: '#FFFFFF', fontSize: 15, fontWeight: '700' },
  headerPct: { color: '#00FF88', fontSize: 22, fontWeight: '900' },
  headerSub: { color: 'rgba(255,255,255,0.4)', fontSize: 10 },
  progressBar: { position: 'absolute', top: 88, left: 0, right: 0, height: 3, backgroundColor: 'rgba(255,255,255,0.1)' },
  progressFill: { height: 3, backgroundColor: '#00FF88' },
  legenda: { position: 'absolute', top: 96, left: 0, right: 0, flexDirection: 'row', justifyContent: 'center', gap: 12, padding: 4, backgroundColor: 'rgba(0,10,30,0.7)' },
  legendaItem: { color: 'rgba(255,255,255,0.7)', fontSize: 9, fontWeight: '600' },
  banner: { position: 'absolute', top: 118, left: 16, right: 16, backgroundColor: 'rgba(0,255,136,.1)', borderRadius: 10, padding: 12, borderWidth: 1, borderColor: 'rgba(0,255,136,0.4)', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  bannerTxt: { color: '#00FF88', fontSize: 12, fontWeight: '700' },
  btnIniciar: { backgroundColor: '#00FF88', borderRadius: 8, padding: 8, paddingHorizontal: 14 },
  btnIniciarTxt: { color: '#001020', fontWeight: '900', fontSize: 12 },
  pin: { width: 30, height: 30, borderRadius: 15, alignItems: 'center', justifyContent: 'center', borderWidth: 2, borderColor: '#001020', elevation: 8, shadowOpacity: 0.8, shadowRadius: 6 },
  pinNum: { color: '#001020', fontWeight: '900', fontSize: 11 },
  depositoPin: { width: 36, height: 36, borderRadius: 18, backgroundColor: 'rgba(0,10,30,0.95)', alignItems: 'center', justifyContent: 'center', borderWidth: 2, borderColor: '#00BFFF' },
  motOuter: { width: 20, height: 20, borderRadius: 10, backgroundColor: 'rgba(0,191,255,0.25)', alignItems: 'center', justifyContent: 'center' },
  motInner: { width: 12, height: 12, borderRadius: 6, backgroundColor: '#00BFFF', borderWidth: 2, borderColor: '#fff' },
  botoesFlut: { position: 'absolute', right: 16, top: 130, gap: 10 },
  btnFlut: { width: 46, height: 46, borderRadius: 23, backgroundColor: 'rgba(0,10,30,0.9)', alignItems: 'center', justifyContent: 'center', elevation: 5, borderWidth: 1, borderColor: 'rgba(0,191,255,0.3)' },
  card: { position: 'absolute', bottom: 20, left: 16, right: 16, backgroundColor: 'rgba(0,10,30,0.97)', borderRadius: 18, padding: 18, elevation: 12, borderWidth: 1 },
  cardLabel: { color: '#00BFFF', fontSize: 9, fontWeight: '800', letterSpacing: 3, marginBottom: 2 },
  seqBadge: { width: 32, height: 32, borderRadius: 16, alignItems: 'center', justifyContent: 'center' },
  seqTxt: { color: '#001020', fontWeight: '900', fontSize: 13 },
  cardNome: { fontSize: 15, fontWeight: '800', color: '#FFFFFF' },
  cardCod: { fontSize: 10, color: '#00BFFF', marginTop: 1 },
  cardEnd: { fontSize: 11, color: 'rgba(255,255,255,0.45)', marginTop: 2 },
  metaTxt: { fontSize: 12, color: 'rgba(255,255,255,0.6)' },
  btnEntrar: { backgroundColor: '#00BFFF', borderRadius: 12, padding: 13, alignItems: 'center' },
  btnEntrarTxt: { color: '#001020', fontWeight: '900', fontSize: 13, letterSpacing: 1 },
  lista: { position: 'absolute', bottom: 0, left: 0, right: 0, backgroundColor: 'rgba(0,10,30,0.98)', borderTopLeftRadius: 20, borderTopRightRadius: 20, maxHeight: height * 0.6, padding: 18, elevation: 12 },
  listaTitulo: { fontSize: 10, fontWeight: '800', color: '#00BFFF', marginBottom: 12, letterSpacing: 3 },
  listaItem: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 11, borderBottomWidth: 1, borderBottomColor: 'rgba(255,255,255,0.06)', paddingLeft: 8 },
  listaNome: { fontSize: 13, fontWeight: '700', color: '#FFFFFF' },
  listaCod: { fontSize: 10, color: 'rgba(0,191,255,0.7)', marginTop: 1 },
  listaEta: { fontSize: 12, color: '#00BFFF', fontWeight: '700' },
});
"""

with open(r'C:\gelocrim-motorista\screens\RotaScreen.js', 'w', encoding='utf-8') as f:
    f.write(rota_screen)
print('RotaScreen.js reescrito!')
